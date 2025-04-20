import sys
from collections import defaultdict
import json

def emit(term, doc_id, tf, doc_len):
    print(f"{term}\t{doc_id}\t{tf}\t{doc_len}")

def main():    
    stats = defaultdict(dict)
    terms = defaultdict(set)
    doc_lens = []
    for line in sys.stdin:
        parts = line.strip().split('\t', 3)
        if len(parts) != 4:
            continue

        tag, field1, field2, field3 = parts

        if tag == "doc":
            doc_id, doc_len, doc_name = field1, field2, field3
            doc_lens.append(int(doc_len))
            print(f"doc\t{doc_id}\t{doc_len}\t{doc_name}")
            
        elif tag == "term":
            term, tf, doc_id = field1, field2, field3
            terms[term].add(doc_id)
            stats[term][doc_id] = int(tf)

    for term, tf_dict in stats.items():
        doc_list = list(terms[term])
        print(f"term\t{term}\t{json.dumps(tf_dict)}\t{json.dumps(doc_list)}")

    N = len(doc_lens)
    avg_len = sum(doc_lens) / N if N > 0 else 0
    print(f"stats\tN\t{N}\tend")
    print(f"stats\tAVG_DOC_LEN\t{avg_len}\tend")


if __name__ == "__main__":
    main()