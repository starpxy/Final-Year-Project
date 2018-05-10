#!/usr/bin/env bash
ps -ef | grep python | grep -v grep
if [ $? -eq 0 ];then
  PID=$(echo `netstat -apn |grep 9609 | awk '{print $NF}'|awk -F '/' '{print $1}'`)
  PID2=$(echo `netstat -apn |grep 9610 | awk '{print $NF}'|awk -F '/' '{print $1}'`)
  kill  $PID
  kill  $PID2
  echo 'Servers has shutdown!'
else
  echo 'Not found socket PID!'
fi