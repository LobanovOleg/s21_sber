#!/bin/bash

input=$1
regex_for_number='^[+-]?[0-9]+([.][0-9]+)?$'

if [[ $input =~ $regex_for_number ]]; then
    echo "Error, invalid input."
else 
    echo "$1"
fi