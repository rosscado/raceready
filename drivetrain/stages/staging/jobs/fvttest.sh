#!/bin/bash
# this script runs integration tests in a Delivery Pipeline job

# install pip for python3
curl -s -S https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user

python3 -m pip install --user -r requirements.txt
python -m pytest --tavern-global-cfg=tests/fvt/config-staging.yaml
