import pytest
from freeListNode import FreeListNode
from markSweepGC import MarkSweepGC
from heapObject import HeapObject


def test_collected_objects_returned_to_free_list():
	o1 = HeapObject(0, 8)

	objects = {1:o1}
	rootset = set()
	free_list = []

	collector = MarkSweepGC(objects, rootset, free_list, settings=None)
	collector.collect()

	assert len(free_list) == 1
	assert free_list[0].heap_index == 0
	assert free_list[0].num_bytes == 8

def test_collects_dead_cycles():
	o1 = HeapObject(0, 8, num_pointers=1)
	o2 = HeapObject(8, 8, num_pointers=1)
	o1.pointers[0] = 2
	o2.pointers[0] = 1

	objects = {1:o1, 2:o2}
	rootset = set()
	free_list = []

	collector = MarkSweepGC(objects, rootset, free_list, settings=None)
	collector.collect()

	live_objects = objects.values()
	assert o1 not in live_objects
	assert o2 not in live_objects

def test_preserves_nested_live_objects():
	o1 = HeapObject(0, 8, num_pointers=1)
	o2 = HeapObject(8, 8, num_pointers=1)
	o1.pointers[0] = 2

	objects = {1:o1, 2:o2}
	rootset = set([1])
	free_list = []

	collector = MarkSweepGC(objects, rootset, free_list, settings=None)
	collector.collect()

	live_objects = objects.values()
	assert o1 in live_objects
	assert o2 in live_objects
