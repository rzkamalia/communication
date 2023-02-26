#!/bin/bash

input_list=("superjunior" "shinee")
# echo "the number of video input ${#input_list[@]}"

SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
MAIN_PATH="$SCRIPT_PATH/flask_thread.py"

iter=1
while [ $iter -le ${#input_list[@]} ]; do
    config=${input_list[iter-1]}
    # echo "running $MAIN_PATH $config"
    python3 $MAIN_PATH $config &
    ((iter++))
done