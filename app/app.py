from cassandra.cluster import Cluster

def main():
    # Connects to the cassandra server
    cluster = Cluster(['cassandra-server'])

    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS simple_search_engine
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)

    session.set_keyspace("simple_search_engine")


    session.execute("""
        CREATE TABLE IF NOT EXISTS vocab (
            term text,
            id text,
            PRIMARY KEY (term, id),
            tf counter
        )
    """)


    session.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            category text,
            key text,
            PRIMARY KEY (category, key),
            value float,
            name text
    )
    """)

    session.execute("""
        CREATE TABLE IF NOT EXISTS term_index (
            term TEXT PRIMARY KEY,
            idx INT
        );
    """)

    rows = session.execute('DESC keyspaces')
    for row in rows:
        print(row)

    session.shutdown()

if __name__ == "__main__":
    main()