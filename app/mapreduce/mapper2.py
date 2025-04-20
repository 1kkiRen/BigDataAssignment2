import sys

def main():
    for line in sys.stdin:
        try:
            line = line.strip()
            print(line)

        except Exception as e:
            sys.stderr.write(f"Error processing line: {line} - {e}\n")

if __name__ == "__main__":
    main()
