#!/bin/bash

# Script to run benchmark required for Assignment #4

tracefile=$1

if [ -z "$tracefile" ]; then
	echo "Usage: ./assignment1 <tracefile>"
	exit 1
fi

heapsize=100000 # start with 100 k

for high_water_percent in 30 70; do 
	for growth_factor in 2.0 3.0; do
		echo "running simulation for $tracefile using: high water = $high_water_percent%, growth factor = $growth_factor x..."
		python app.py $heapsize $high_water_percent $growth_factor < $tracefile
	done
done
