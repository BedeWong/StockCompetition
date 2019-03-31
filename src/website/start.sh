#! /bin/bash

#ps aux | grep  "python3 server" | grep -v grep | awk '{print $2}' | xargs kill   #  kill

nohup python3 server.py &									# start
