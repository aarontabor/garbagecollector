import pytest
from outOfMemoryException import OutOfMemoryException
from firstFitAllocator import FirstFitAllocator
from freeListNode import FreeListNode


@pytest.fixture
def simple_allocator():
	n1 = FreeListNode(0,1)
	n2 = FreeListNode(2,3)
	n3 = FreeListNode(9,3)
	return FirstFitAllocator([n1, n2, n3])

def test_throws_exception_when_empty_free_list():
	f = FirstFitAllocator([])
	with pytest.raises(OutOfMemoryException):
		f.allocate(1)

def test_allocates_in_first_fit_order(simple_allocator):
	assert simple_allocator.allocate(3) == 2

def test_throws_exception_when_no_appropriate_free_node(simple_allocator):
	with pytest.raises(OutOfMemoryException):
		simple_allocator.allocate(4)

def test_creates_new_node_from_remaining_memory(simple_allocator):
	simple_allocator.allocate(2) == 2
	free_list = simple_allocator.free_list
	assert free_list[1].heap_index == 4
	assert free_list[1].num_bytes == 1

def test_maintains_ascending_heap_order(simple_allocator):
	simple_allocator.free(6, 1)
	free_list = simple_allocator.free_list
	assert free_list[2].heap_index == 6
	assert free_list[2].num_bytes == 1


@pytest.fixture
def adjacent_allocator():
	n1 = FreeListNode(0,1)
	n2 = FreeListNode(2,1)
	n3 = FreeListNode(5,1)
	return FirstFitAllocator([n1, n2, n3])

def test_preceeding_adjacent_nodes_are_merged(adjacent_allocator):
	adjacent_allocator.free(3, 1)
	free_list = adjacent_allocator.free_list
	assert len(free_list) == 3
	assert free_list[1].heap_index == 2
	assert free_list[1].num_bytes == 2

def test_proceeding_adjacent_nodes_are_merged(adjacent_allocator):
	adjacent_allocator.free(4, 1)
	free_list = adjacent_allocator.free_list
	assert len(free_list) == 3
	assert free_list[2].heap_index == 4
	assert free_list[2].num_bytes == 2

def test_three_adjacent_nodes_are_merged(adjacent_allocator):
	adjacent_allocator.free(3, 2)
	free_list = adjacent_allocator.free_list
	assert len(free_list) == 2
	assert free_list[1].heap_index == 2
	assert free_list[1].num_bytes == 4
