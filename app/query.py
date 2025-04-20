import sys
import re
import os
import math
from collections import defaultdict
from cassandra.cluster import Cluster

def main():
    if len(sys.argv) < 2:
        print("Usage: query.py <query string>", file=sys.stderr)
        sys.exit(1)
    query = sys.argv[1]
    query_terms = re.findall(r'\w+', query.lower())

    cluster = Cluster(['cassandra-server'])
    session = cluster.connect('simple_search_engine')

    stats_rows = session.execute(
        "SELECT key, value FROM stats WHERE category = 'stats'")
    stats = {row.key: row.value for row in stats_rows}
    N = stats.get('N', 1)
    avg_doc_len = stats.get('AVG_DOC_LEN', 1)

    doc_stats_rows = session.execute(
        "SELECT key, value FROM stats WHERE category = 'doc'")
    doc_lens = {row.key: float(row.value) for row in doc_stats_rows}
    
    doc_scores = defaultdict(float)
    k1, b = 1.5, 0.75

    for term in query_terms:
        df_row = session.execute(
            "SELECT COUNT(id) AS df FROM vocab WHERE term = %s", (term,)
        ).one()
        
        df = df_row.df if df_row and df_row.df else 1
        idf = math.log(1 + ((N - df + 0.5) / (df + 0.5)))
        
        rows = session.execute(
            "SELECT id, tf FROM vocab WHERE term = %s", (term,)
        )
        
        for row in rows:
            doc_id, tf = row.id, row.tf
            doc_len = doc_lens.get(doc_id, avg_doc_len)
            score = idf * (tf * (k1 + 1)) / (
                tf + k1 * (1 - b + b * doc_len / avg_doc_len)
            )
            doc_scores[doc_id] += score

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    doc_titles = {}

    for fname in os.listdir(data_dir):
        if fname.endswith('.txt'):
            doc_id, rest = fname.split('_', 1)
            title = rest.rsplit('.txt', 1)[0].replace('_', ' ')
            doc_titles[doc_id] = title

    results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:10]

    print("Top 10 relevant documents:")
    for doc_id, score in results:
        title = doc_titles.get(doc_id, "<unknown>")
        print(f"{doc_id}\t{title}\t{score:.6f}")

if __name__ == "__main__":
    main()