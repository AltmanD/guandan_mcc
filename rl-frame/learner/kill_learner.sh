#!/bin/bash
# ps -ef | grep learner.py | awk '{print $2}' | xargs kill -9
ps aux|grep python|grep -v grep|cut -c 9-15|xargs kill -9
