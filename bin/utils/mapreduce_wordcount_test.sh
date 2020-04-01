#!/bin/bash

hdfs dfs -rm -r output
yarn jar ~/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar wordcount "books/*" output
hdfs dfs -head output/part-r-00000
echo -e "\nIf you whould like to view the whole results execute > hdfs dfs -cat output/part-r-00000 | less"