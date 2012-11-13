#!/bin/sh
PARENT_PID=$$
(sleep 20 && kill -TERM $PARENT_PID > /dev/null 2>&1)&

PYTHONPATH=../ofxparse python main.py > html/result.txt.tmp && mv html/result.txt.tmp html/result.txt