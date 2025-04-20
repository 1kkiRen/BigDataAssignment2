#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: search.sh <query string>"
    exit 1
fi

query="$*"

source /opt/venv/bin/activate

export PYSPARK_DRIVER_PYTHON=$(which python)
export PYSPARK_PYTHON=$(which python)

echo "Query: $query"
spark-submit --master yarn query.py "$query"

deactivate