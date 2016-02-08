#!/bin/bash

# Script to run benchmarks required for Assignment #5
#
#	1. MarkSweep (no grow) with heapsize <N>
# 2. Copying with total heapsize <N> (each space only has 1/2 <N>)
# 3. Copying with total heapsize 2 * <N> (each space has <N>)

tracefile=$1

if [ -z "$tracefile" ]; then
	echo "Usage: ./assignment1 <tracefile>"
	exit 1
fi

N=12000000 # 12 million

# Benchmark 1
echo "running $tracefile using mark_sweep with heapsize: $N..."
python app.py --heap_size $N mark_sweep_grow < $tracefile # growth_factor is implicitly 1.0

# Benchmark 2
echo "running $tracefile using copying with heapsize: $N..."
python app.py --heap_size $N copying < $tracefile

# Benchmark 3
echo "running $tracefile using copying with heapsize: $((N*2))..."
python app.py --heap_size $((N*2)) copying < $tracefile
