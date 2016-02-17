import pytest
from heapObject import HeapObject
from recyclerGC import RecyclerGC


class MockSettings:
	pass

@pytest.fixture
def settings():
	return MockSettings()


def test_non_candidates_are_ignored(settings):
	o1 = HeapObject(0, 8)

	o1.referenceCount = 0
	o1.color = 'black' # not a candidate

	objects = {1: o1}
	rootset = set()
	free_list = []

	collector = RecyclerGC(objects, rootset, free_list, settings)
	collector.collect()

	live_objects = objects.values()
	assert o1 in live_objects

def test_dead_candidates_are_collected(settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(10, 8)

	# dead object cycle
	o1.referenceCount = 1
	o2.referenceCount = 1
	o1.pointers[0] = 2
	o2.pointers[0] = 1
	o1.color = 'purple'
	o2.color = 'purple'

	objects = {1: o1, 2: o2}
	rootset = set([])
	free_list = []

	collector = RecyclerGC(objects, rootset, free_list, settings)
	collector.collect()

	live_objects = objects.values()
	assert o1 not in live_objects
	assert o2 not in live_objects

	assert len(free_list) == 2
	assert free_list[0].heap_index == 0
	assert free_list[1].heap_index == 10

def test_live_candidates_are_preserved(settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(10, 8)

	# dead object cycle
	o1.referenceCount = 2
	o2.referenceCount = 1
	o1.pointers[0] = 2
	o2.pointers[0] = 1
	o1.color = 'purple'
	o2.color = 'purple'

	objects = {1: o1, 2: o2}
	rootset = set([1])
	free_list = []

	collector = RecyclerGC(objects, rootset, free_list, settings)
	collector.collect()

	live_objects = objects.values()
	assert o1 in live_objects
	assert o2 in live_objects

	assert len(free_list) == 0

def test_mixed_cycle(settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(10, 8, num_pointers=2)

	# o2 is only referenced by itself
	o1.referenceCount = 2
	o2.referenceCount = 1
	o2.pointers[0] = 1
	o2.pointers[1] = 2
	o1.color = 'purple'
	o2.color = 'purple'

	objects = {1: o1, 2: o2}
	rootset = set([1])
	free_list = []

	collector = RecyclerGC(objects, rootset, free_list, settings)
	collector.collect()

	live_objects = objects.values()
	assert o1 in live_objects
	assert o2 not in live_objects

	assert len(free_list) == 1
	assert free_list[0].heap_index == 10
