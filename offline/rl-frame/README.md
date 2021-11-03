# RL Framework

A distributed reinforcement learning framework

## Getting Started

```shell script
export HOROVOD_GPU_OPERATIONS=NCCL
```
## Environment Install (conda or docker)
1. conda env (do not available in windows) 
```shell script
conda env create -f learner/build/conda/env_linux.yaml
```
2. docker env
```shell script
cd learner/build/docker/
docker build -t $name:$tag .
```
### Change config in *learner/examples/xxx/xxxx.yaml* and *actor/examples/xxx/xxxx.yaml*
### Modify the startup script, and start it 
```shell script
bash start.bash
```

### If want kill all process
```shell script
bash kill.bash
```
### Default parameters saved in learner/examples/xxx/xxxx.yaml and actor/examples/xxx/xxxx.yaml