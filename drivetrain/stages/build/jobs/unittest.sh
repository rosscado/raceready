#!/bin/bash
# this script runs the application's unit tests in a Delivery Pipeline job

# install pip for python3
curl -s -S https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user

# run pip and python with python3
python3 --version
python3 -m pip --version

python3 -m pip install --user -r requirements.txt
python3 -m pytest --ignore=tests/fvt # unit tests only
