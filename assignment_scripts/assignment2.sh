#!/bin/bash

# Script to run benchmark required for Assignment #1

tracefile=$1

if [ -z "$tracefile" ]; then
	echo "Usage: ./assignment1 <tracefile>"
	exit 1
fi

for i in 500 1000 5000 5350 6000 10000; do
	echo "running simulation for $tracefile using a $i byte heap..."
	python app.py $i < $tracefile
done
