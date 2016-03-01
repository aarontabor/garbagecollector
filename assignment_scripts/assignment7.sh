#!/bin/bash

# Script to run benchmarks required for Assignment #7
#
# Optimizations attempted:
# 	- next fit allocation
#
# I should see the biggest performance gains using a mark-sweep grow approach
# (as this will produce fragmentation)
#

tracefile=$1

if [ -z "$tracefile" ]; then
	echo "Usage: ./assignment1 <tracefile>"
	exit 1
fi

N=15000000

# Benchmark 1
echo "running $tracefile using first-fit allocation: $N..."
python app.py --heap_size $N --allocator first_fit --write_barrier reference_counting mark_sweep_grow < $tracefile

# Benchmark 2
echo "running $tracefile using next-fit allocation: $N..."
python app.py --heap_size $N --allocator next_fit --write_barrier reference_counting mark_sweep_grow < $tracefile
