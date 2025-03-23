#! /bin/bash

if [ -d ".venv" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .venv/bin/activate

# run main py file which has flask instance
python3 main.py

# deactivate virtual env stops 
deactivate