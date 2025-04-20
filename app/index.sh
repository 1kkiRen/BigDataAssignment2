#!/bin/bash

INPUT=$1
hdfs dfs -ls /index/data

echo "Start indexing"
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files /app/mapreduce/mapper1.py,/app/mapreduce/reducer1.py \
  -archives /app/.venv.tar.gz#.venv \
  -D mapreduce.framework.name=yarn \
  -mapper ".venv/bin/python mapper1.py" \
  -reducer ".venv/bin/python reducer1.py" \
  -input "$INPUT" \
  -output /tmp/index/indexer \

hdfs dfs -ls /tmp/index/indexer
hdfs dfs -cat /tmp/index/indexer/part-* > indexer_output.txt

echo "Transfer to Cassandra"
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files /app/mapreduce/mapper2.py,/app/mapreduce/reducer2.py \
  -archives /app/.venv.tar.gz#.venv \
  -D mapreduce.framework.name=yarn \
  -mapper ".venv/bin/python mapper2.py" \
  -reducer ".venv/bin/python reducer2.py" \
  -input /tmp/index/indexer/part-* \
  -output /tmp/index/transfer \

hdfs dfs -ls /
