import pytest
from freeListStatsGenerator import FreeListsStatsGenerator
from freeListNode import FreeListNode


class MockSettings:
	pass

@pytest.fixture
def mock_settings():
	settings = MockSettings()
	settings.heap_size = 100
	return settings


def test_percent_when_heap_empty(mock_settings):
	n = FreeListNode(0,100)
	s = FreeListsStatsGenerator(mock_settings, [n])
	assert s.percent_free() == 100
	assert s.percent_used() == 0

def test_percent_when_heap_full(mock_settings):
	s = FreeListsStatsGenerator(mock_settings, [])
	assert s.percent_free() == 0
	assert s.percent_used() == 100

def test_percent_when_heap_partial(mock_settings):
	n1 = FreeListNode(0,22)
	n2 = FreeListNode(50,14)
	s = FreeListsStatsGenerator(mock_settings, [n1, n2])
	assert s.percent_free() == 36
	assert s.percent_used() == 64

def test_average_node_size(mock_settings):
	n1 = FreeListNode(0,10)
	n2 = FreeListNode(40,30)
	n3 = FreeListNode(80,20)
	s = FreeListsStatsGenerator(mock_settings, [n1, n2, n3])
	assert s.average_node_size() == 20

def test_average_node_size_returns_sane_value_with_full_heap(mock_settings):
	s = FreeListsStatsGenerator(mock_settings, [])
	assert s.average_node_size() == 0
