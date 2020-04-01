#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

bash "$SCRIPTPATH/stop_hdfs.sh"

if hash hdfs 2>/dev/null; then
  yes | hdfs namenode -format
fi

username=hadoop

for node in $(cat /etc/hosts | grep 'master\|worker' | awk '{ print $2 }')
do
  if [[ $node == *"master"* ]]; then
    rm -rf ~/hadoop ~/java ~/*.gz
    rm -rf .ssh;
    if [ -d ~/data ]; then
      rm -rf ~/data
    fi
  else
    ssh -q "$username@$node" << EOF
    if [ -f ~/hosts ]; then
      cat ~/hosts > /etc/hosts;
    fi
    if [ -f ~/.profile2 ]; then
      cat .profile2 > .profile;
      rm .profile2;
    fi
    rm -rf ~/hadoop ~/java ~/*.gz;
    rm -rf .ssh;
    if [ -d ~/data ]; then
      rm -rf ~/data
    fi
EOF
  fi
done