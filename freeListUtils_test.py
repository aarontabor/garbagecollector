import pytest
from freeListNode import FreeListNode
from freeListUtils import add_node


@pytest.fixture
def free_list():
	n1 = FreeListNode(0,1)
	n2 = FreeListNode(2,1)
	n3 = FreeListNode(6,1)
	return [n1, n2, n3]

def test_maintains_ascending_heap_order(free_list):
	n = FreeListNode(4, 1)
	add_node(free_list, n)
	assert len(free_list) == 4
	assert free_list[2] == n

def test_preceeding_adjacent_nodes_are_merged(free_list):
	n = FreeListNode(3, 1)
	add_node(free_list, n)
	assert len(free_list) == 3
	assert free_list[1].heap_index == 2
	assert free_list[1].num_bytes == 2

def test_proceeding_adjacent_nodes_are_merged(free_list):
	n = FreeListNode(5, 1)
	add_node(free_list, n)
	assert len(free_list) == 3
	assert free_list[2].heap_index == 5
	assert free_list[2].num_bytes == 2

def test_three_adjacent_nodes_are_merged(free_list):
	n = FreeListNode(3, 3)
	add_node(free_list, n)
	assert len(free_list) == 2
	assert free_list[1].heap_index == 2
	assert free_list[1].num_bytes == 5

