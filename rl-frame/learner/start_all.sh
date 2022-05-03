#!/bin/bash
# sshpass ssh root@172.15.15.3 "bash /home/luyd/guandan/actor_n/start.sh"
# nohup python -u learner.py > ./learner_out.log 2>&1 &
for i in {3..23}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done

nohup python -u learner.py > ./learner_out.log 2>&1 &

for i in {24..83}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done
