import pytest
from freeListNode import FreeListNode
from markSweepGrowGC import MarkSweepGrowGC
from heapObject import HeapObject


class MockSettings:
	pass

@pytest.fixture
def mock_settings():
	settings = MockSettings()
	settings.heap_size = 50
	settings.high_water_percent = 100
	settings.growth_factor = 1.0
	return settings

def test_collected_objects_returned_to_free_list(mock_settings):
	o1 = HeapObject(0, 8)

	objects = {1:o1}
	rootset = set()
	free_list = []

	collector = MarkSweepGrowGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	assert len(free_list) == 1
	assert free_list[0].heap_index == 0
	assert free_list[0].num_bytes == 8

def test_collects_dead_cycles(mock_settings):
	o1 = HeapObject(0, 8, num_pointers=1)
	o2 = HeapObject(8, 8, num_pointers=1)
	o1.pointers[0] = 2
	o2.pointers[0] = 1

	objects = {1:o1, 2:o2}
	rootset = set()
	free_list = []

	collector = MarkSweepGrowGC(objects, rootset, free_list, settings=mock_settings)
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

	collector = MarkSweepGrowGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	live_objects = objects.values()
	assert o1 in live_objects
	assert o2 in live_objects

def test_heap_grows_when_sufficient_utilization(mock_settings):
	mock_settings.heap_size = 100
	mock_settings.high_water_percent = 50
	mock_settings.growth_factor = 2.0
	
	o1 = HeapObject (0, 80)

	objects = {1:o1}
	rootset = set([1])
	free_list = [FreeListNode(80, 20)]

	collector = MarkSweepGrowGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	# Heap utilization is 80%, heap should grow by 2.0x
	assert mock_settings.heap_size == 200

def test_heap_doesnt_grows_when_insufficient_utilization(mock_settings):
	mock_settings.heap_size = 100
	mock_settings.high_water_percent = 50
	mock_settings.growth_factor = 2.0
	
	o1 = HeapObject (0, 8)

	objects = {1:o1}
	rootset = set([1])
	free_list = [FreeListNode(8, 92)]

	collector = MarkSweepGrowGC(objects, rootset, free_list, settings=mock_settings)
	collector.collect()

	# Heap utilization is only 8%, heap should not grow
	assert mock_settings.heap_size == 100
