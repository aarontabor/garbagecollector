import pytest
from freeListNode import FreeListNode
from copyingGC import CopyingGC
from heapObject import HeapObject


class MockSettings:
	pass

@pytest.fixture
def mock_settings():
	settings = MockSettings()
	settings.heap_size = 100
	return settings


# Collect Tests
def test_collects_dead_cycles(mock_settings):
	o1 = HeapObject(0, 8, num_pointers=1)
	o2 = HeapObject(8, 8, num_pointers=1)
	o1.pointers[0] = 2
	o2.pointers[0] = 1

	objects = {1:o1, 2:o2}
	rootset = set()
	free_list = []

	collector = CopyingGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	live_objects = objects.values()
	assert o1 not in live_objects
	assert o2 not in live_objects

def test_preserves_nested_live_objects(mock_settings):
	o1 = HeapObject(0, 8, num_pointers=1)
	o2 = HeapObject(8, 8, num_pointers=1)
	o1.pointers[0] = 2

	objects = {1:o1, 2:o2}
	rootset = set([1])
	free_list = []

	collector = CopyingGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	live_objects = objects.values()
	assert o1 in live_objects
	assert o2 in live_objects

def test_collected_objects_get_copied(mock_settings):
	o = HeapObject(0, 8)

	objects = {1: o}
	rootset = set([1])
	free_list = [FreeListNode(0, mock_settings.heap_size)]

	collector = CopyingGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	assert o.heap_index == 50
	assert o.size == 8

def test_free_space_accounts_for_live_objects(mock_settings):
	o = HeapObject(0, 8)

	objects = {1: o}
	rootset = set([1])
	free_list = [FreeListNode(0, mock_settings.heap_size)]

	collector = CopyingGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	assert len(free_list) == 1
	assert free_list[0].heap_index == 58
	assert free_list[0].num_bytes == 42 


# Helper Method Tests
def test_delete(mock_settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(8, 8)

	objects = {1: o1, 2: o2}
	rootset = set()
	free_list = []

	o1.marked = True
	o2.marked = False

	collector = CopyingGC(objects, rootset, free_list, settings=mock_settings)
	collector.delete()

	live_objects = objects.values()
	assert o1 in live_objects
	assert o2 not in live_objects

	assert not o1.marked # resets flag

def test_swap_spaces(mock_settings):
	objects = {}
	rootset = set()
	free_list = [FreeListNode(0, mock_settings.heap_size)]

	collector = CopyingGC(objects, rootset, free_list, settings=mock_settings)

	# Initially use first half of heap
	assert len(free_list) == 1
	assert free_list[0].heap_index == 0
	assert free_list[0].num_bytes == 50

	collector.swap_spaces()

	# swap to second half
	assert len(free_list) == 1
	assert free_list[0].heap_index == 50
	assert free_list[0].num_bytes == 50

	collector.swap_spaces()

	# back to first half again
	assert len(free_list) == 1
	assert free_list[0].heap_index == 0
	assert free_list[0].num_bytes == 50
