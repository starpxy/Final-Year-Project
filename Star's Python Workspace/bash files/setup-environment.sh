#!/usr/bin/env bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
export PATH=/home/142017156/.local/bin:$PATH
pip3 install --user sklearn
pip3 install --user numpy
pip3 install --user scipy