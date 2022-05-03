#!/bin/bash
#docker run -itd --gpus all --network=guandanNet --ip 172.15.15.2 --name guandan_learner -v /home/luyd/guandan/:/home/luyd/guandan -w /home/luyd/guandan/ nvcr.io/nvidia/tensorflow:22.02-tf1-py3
for i in {4..83}
do
    docker run -itd --network=guandanNet --ip 172.15.15.$i --name guandan_actor_$i -v /home/luyd/log/log$i:/home/root/log -v /home/luyd/guandan:/home/luyd/guandan -w /home/luyd/guandan  guandan_actor:v2 /bin/bash
done
