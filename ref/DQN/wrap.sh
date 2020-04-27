#!/bin/sh

python3 run.py --mode train -i $1 -e 10 > log.txt
weights=$(tail -6 log.txt | head -1)
echo $weights 
python3 run.py --mode test --weights $weights -e 20 > log.txt
python3 get_result.py
