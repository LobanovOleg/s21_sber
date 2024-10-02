#!bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 setup.py build_ext --inplace
python3 test_mul_perf.py --size 10