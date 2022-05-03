#!/bin/bash
for i in {5..8}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done

for i in {11..12}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done

for i in {19..20}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done
for i in {22..24}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done
sshpass ssh root@172.15.15.31 "bash /home/luyd/guandan/actor_n/start.sh"
sshpass ssh root@172.15.15.33 "bash /home/luyd/guandan/actor_n/start.sh"
sshpass ssh root@172.15.15.35 "bash /home/luyd/guandan/actor_n/start.sh"
sshpass ssh root@172.15.15.48 "bash /home/luyd/guandan/actor_n/start.sh"
sshpass ssh root@172.15.15.52 "bash /home/luyd/guandan/actor_n/start.sh"
sshpass ssh root@172.15.15.57 "bash /home/luyd/guandan/actor_n/start.sh"
sshpass ssh root@172.15.15.55 "bash /home/luyd/guandan/actor_n/start.sh"


for i in {60..61}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done
for i in {63..65}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done
sshpass ssh root@172.15.15.68 "bash /home/luyd/guandan/actor_n/start.sh"

for i in {70..72}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done
for i in {78..80}
do
        sshpass ssh root@172.15.15.$i "bash /home/luyd/guandan/actor_n/start.sh"
        echo $i
        sleep 0.1s
done