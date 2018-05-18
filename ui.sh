#!/bin/bash
tmux new-session -d "./chat.py -r $@"
tmux split-window -v "./chat.py $@"
tmux attach \; resize-pane -y 2
