#!/bin/bash
nohup /home/luyd/guandan/actor_n/guandan 1000000000000 >/dev/null 2>&1 &
sleep 0.5s
nohup /root/miniconda3/envs/guandan/bin/python -u /home/luyd/guandan/actor_n/actor.py > /home/luyd/actor_out.log 2>&1 &
sleep 0.5s
nohup /root/miniconda3/envs/guandan/bin/python -u /home/luyd/guandan/actor_n/game.py > /home/luyd/game_out.log 2>&1 &