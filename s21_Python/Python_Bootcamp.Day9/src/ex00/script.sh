#!bin/bash

python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install dist/calculator-1.0.tar.gz
python3 test.py