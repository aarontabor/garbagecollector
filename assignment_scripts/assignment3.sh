#!/bin/bash

# Script to run benchmark required for Assignment #3

tracefile=$1

if [ -z "$tracefile" ]; then
	echo "Usage: ./assignment1 <tracefile>"
	exit 1
fi

allocations=`cat $tracefile | grep '^a' | wc -l`
echo "$tracefile allocates a total of $allocations objects."
echo

for i in 1073741824; do # 1 GB
	echo "running simulation for $tracefile using a $i byte heap..."
	python app.py $i < $tracefile
done
