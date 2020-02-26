#!/bin/bash

echo "date,open,high,low,close,volume,a1,a2,Name" > mixer.csv
cd src
files=$(ls *.csv)
for file in $files
do
	tail -n +2 $file >> ../mixer.csv
done