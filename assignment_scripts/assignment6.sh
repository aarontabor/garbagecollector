#!/bin/bash

# Script to run benchmarks required for Assignment #6
#
# 1. Reference Counting & MarkSweep with heapsize <N>
# 1. Recycler with heapsize <N>

tracefile=$1

if [ -z "$tracefile" ]; then
	echo "Usage: ./assignment1 <tracefile>"
	exit 1
fi

N=15000000

# Benchmark 1
echo "running $tracefile using reference_counting & mark_sweep with heapsize: $N..."
python app.py --heap_size $N --write_barrier reference_counting mark_sweep_grow < $tracefile

# Benchmark 2
echo "running $tracefile using recycler with heapsize: $N..."
python app.py --heap_size $N --write_barrier recycler recycler < $tracefile
