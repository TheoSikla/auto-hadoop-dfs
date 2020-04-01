#!/bin/bash

hdfs dfs -mkdir -p /user/hadoop
hdfs dfs -mkdir books
cd /home/hadoop
wget -O alice.txt https://www.gutenberg.org/files/11/11-0.txt
wget -O holmes.txt https://www.gutenberg.org/files/1661/1661-0.txt
wget -O frankenstein.txt https://www.gutenberg.org/files/84/84-0.txt
hdfs dfs -put alice.txt holmes.txt frankenstein.txt books
hdfs dfs -ls books
