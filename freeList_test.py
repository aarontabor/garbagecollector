import pytest
from freeList import FreeList
from freeListNode import FreeListNode


@pytest.fixture
def simple_free_list():
	n1 = FreeListNode(0,1)
	n2 = FreeListNode(2,2)
	n3 = FreeListNode(7,2)
	return FreeList([n1, n2, n3])

def test_pops_none_when_empty():
	f = FreeList()
	assert f.pop_node(1) == None

def test_pops_in_first_fit_order(simple_free_list):
	n = simple_free_list.pop_node(2)
	assert n.heap_index == 2

def test_pops_none_when_no_suitable_node(simple_free_list):
	assert simple_free_list.pop_node(3) == None

def test_maintains_ascending_heap_order(simple_free_list):
	n = FreeListNode(5,1)
	simple_free_list.add_node(n)
	assert simple_free_list[2] == n


@pytest.fixture
def adjacent_free_list():
	n1 = FreeListNode(0,1)
	n2 = FreeListNode(2,1)
	n3 = FreeListNode(5,1)
	return FreeList([n1, n2, n3])

def test_preceeding_adjacent_nodes_are_merged(adjacent_free_list):
	n = FreeListNode(3,1)
	adjacent_free_list.add_node(n)
	assert len(adjacent_free_list) == 3
	assert adjacent_free_list[1].heap_index == 2
	assert adjacent_free_list[1].num_bytes == 2

def test_proceeding_adjacent_nodes_are_merged(adjacent_free_list):
	n = FreeListNode(4,1)
	adjacent_free_list.add_node(n)
	assert len(adjacent_free_list) == 3
	assert adjacent_free_list[2].heap_index == 4
	assert adjacent_free_list[2].num_bytes == 2

def test_three_adjacent_nodes_are_merged(adjacent_free_list):
	n = FreeListNode(3,2)
	adjacent_free_list.add_node(n)
	assert len(adjacent_free_list) == 2
	assert adjacent_free_list[1].heap_index == 2
	assert adjacent_free_list[1].num_bytes == 4
