#!/bin/bash
for i in {4..83}
do
	docker rm -f guandan_actor_$i
done

