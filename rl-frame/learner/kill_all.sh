#!/bin/bash
for i in {3..83}
do
	sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/kill.sh"
done
bash kill_learner.sh
