ps aux | grep actor.py | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep learner.py | grep -v grep | awk '{print $2}' | xargs kill -9