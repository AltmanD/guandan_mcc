#!/bin/bash
ps -ef | grep guandan | awk '{print $2}' | xargs kill -9
ps -ef | grep server | awk '{print $2}' | xargs kill -9
ps aux|grep python|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef | grep actor | awk '{print $2}' | xargs kill -9
ps -ef | grep game | awk '{print $2}' | xargs kill -9
ps -ef | grep python | awk '{print $2}' | xargs kill -9
rm /home/luyd/game_out.log
