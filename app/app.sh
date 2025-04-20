#!/bin/bash

# Start ssh server
service ssh restart 

# Starting the services
bash start-services.sh

source /opt/venv/bin/activate

venv-pack -o .venv.tar.gz

# Build the Cassandra
python app.py
deactivate

# Collect data
bash prepare_data.sh

# Run the indexer
bash index.sh /index/data/part-*

# Run the rankers
bash search.sh "this is a query!"
bash search.sh "artificial intelligence"
bash search.sh "big data"
