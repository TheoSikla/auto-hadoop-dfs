#!/bin/bash

yes | hdfs namenode -format

username=hadoop

for node in $(cat /etc/hosts | grep 'master\|worker' | awk '{ print $2 }')
do
  if [[ $node == *"master"* ]]; then
    cat /etc/hosts;
  else
    ssh -q "$username@$node" << EOF
    if [ -f ~/hosts ]; then
      cat hosts > /etc/hosts;
    fi
    if [ -f ~/.profile2 ]; then
      cat .profile2 > .profile;
      rm .profile2;
    fi
    rm -rf /home/hadoop/*;
    rm -rf .ssh;
EOF
  fi
done