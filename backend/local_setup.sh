#! /bin/bash

echo "==============================="
echo "Welcome to flask Devlopment. This"
echo "is local setup bash script which"
echo "will checks or create .env and then"
echo "install all the required libraries"
echo "from requirements.txt file."
echo "You can rerun this without any issue."
echo "^()^ Happy learning ^()^"

if [ -d ".venv" ];
then
    echo ".venv folder exits. Installing using pip"
else
    echo "creating .venv and install using pip"
    python3 -m venv .venv
fi

. .venv/bin/activate

pip install -r requirements.txt
echo "work done deactivating .venv"
deactivate