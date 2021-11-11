#!/bin/bash
ps -ef | grep guandan | awk '{print $2}' | xargs kill -9
ps -ef | grep client.py | awk '{print $2}' | xargs kill -9
