#!/bin/bash
./guandan 100 > ./server_out.log 2>&1 &
sleep 1s
# 启动虚拟环境，若使用本地环境则删除此句
source activate guandan
nohup python -u client.py > ./client_out.log 2>&1 &