#! /bin/bash

if [ -d ".venv" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi


. .venv/bin/activate
celery -A main.celery worker -l info
deactivate