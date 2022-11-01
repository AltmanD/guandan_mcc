# Guandan
## Insatll 
### lib needs:

linux20.04

python=3.8

tensorflow=1.15.5

numpy=1.18.5

websocket(ws4py)=0.5.1

pyarrow=5.0.0

pyzmq=22.3.0

## Run
### actor
`python actor_n/actor.py`

### learner
`python learner/learner.py`

## Eval

`bash wintest/testmodel.sh`

## Showdown

follow these steps:

in terminal1

`cd guandan_mcc/showdown`

`./guandan 1`

in terminal2

`cd guandan_mcc/showdown/clients`

`python3 client1.py &`

`python3 client2.py &`

`python3 client3.py &`

in terminal3

`python3 client4.py &`

in terminal2

`python3 actor.py`

in terminal3

`python3 showdown_actor.py`

and have fun!
