import sys
import os
import re
from collections import Counter

def simple_tokenize(text):
    """Simple tokenization: lowercase, remove punctuation, split on whitespace"""
    
    tokens = re.findall(r"\w+", text.lower())
    return tokens


def preprocess_text(text):
    """Preprocess text: tokenize, remove stopwords"""
    
    tokens = simple_tokenize(text)
    stopwords = set(['the', 'is', 'in', 'and', 'to', 'a'])
    tokens = [token for token in tokens if token not in stopwords]
    
    return tokens

def main():
    for line in sys.stdin:
        try:
            if not line:
                continue

            line_parts = line.split('\t', 2)

            if len(line_parts) == 3:
                doc_id = line_parts[0].strip()
                title = line_parts[1].strip()
                content = line_parts[2].strip()
            else:
                doc_id = os.environ.get('map_input_file', 'unknown')
                if doc_id != 'unknown':
                    doc_id = os.path.basename(doc_id)
                content = line

            tokens = preprocess_text(content)

            term_counts = Counter(tokens)

            print(f"doc\t{doc_id}\t{len(tokens)}\t{title}")
            for term in term_counts:
                print(f"term\t{term}\t{term_counts[term]}\t{doc_id}")

        except Exception as e:
            pass

if __name__ == "__main__":
    main()