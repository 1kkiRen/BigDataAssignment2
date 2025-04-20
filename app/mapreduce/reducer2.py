import sys
import json
from cassandra.cluster import Cluster

def main():
    cluster = Cluster(["cassandra-server"])
    session = cluster.connect("simple_search_engine")

    update_tf = session.prepare("""
        UPDATE vocab SET tf = tf + ? WHERE term = ? AND id = ?
    """)
    insert_stats = session.prepare("""
        INSERT INTO stats (category, key, value, name) VALUES (?, ?, ?, ?)
    """)

    for line in sys.stdin:
        parts = line.strip().split("\t", 3)
        
        if len(parts) < 2:
            continue
        
        tag = parts[0]
        
        if tag == "doc" and len(parts) == 4:
            doc_id, doc_len, doc_name = parts[1:]
            session.execute(insert_stats, (tag, doc_id, float(doc_len), doc_name))
            
        elif tag == "stats" and len(parts) == 4:
            key, value = parts[1:3]
            
            try:
                session.execute(insert_stats, (tag, key, float(value), "stats_values"))
                
            except Exception:
                continue
            
        elif tag == "term" and len(parts) == 4:
            term, tf_dict = parts[1:3]
            
            try:
                tf_dict = json.loads(tf_dict)
                
            except json.JSONDecodeError:
                continue
            
            for doc_id, tf in tf_dict.items():
                session.execute(update_tf, (int(tf), term, doc_id))

    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()