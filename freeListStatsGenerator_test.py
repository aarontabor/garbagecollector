import pytest
from freeListStatsGenerator import FreeListsStatsGenerator
from freeListNode import FreeListNode


def test_percent_when_heap_empty():
	n = FreeListNode(0,100)
	s = FreeListsStatsGenerator(100, [n])
	assert s.percent_free() == 100
	assert s.percent_used() == 0

def test_percent_when_heap_full():
	s = FreeListsStatsGenerator(100, [])
	assert s.percent_free() == 0
	assert s.percent_used() == 100

def test_percent_when_heap_partial():
	n1 = FreeListNode(0,22)
	n2 = FreeListNode(50,14)
	s = FreeListsStatsGenerator(100, [n1, n2])
	assert s.percent_free() == 36
	assert s.percent_used() == 64

def test_average_node_size():
	n1 = FreeListNode(0,10)
	n2 = FreeListNode(40,30)
	n3 = FreeListNode(80,20)
	s = FreeListsStatsGenerator(100, [n1, n2, n3])
	assert s.average_node_size() == 20
