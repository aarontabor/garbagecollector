import pytest
from outOfMemoryException import OutOfMemoryException
from firstFitAllocator import FirstFitAllocator
from freeListNode import FreeListNode


@pytest.fixture
def allocator():
	n1 = FreeListNode(0,1)
	n2 = FreeListNode(2,3)
	n3 = FreeListNode(9,3)
	return FirstFitAllocator([n1, n2, n3], settings=None)

def test_throws_exception_when_empty_free_list():
	f = FirstFitAllocator([], settings=None)
	with pytest.raises(OutOfMemoryException):
		f.allocate(1)

def test_allocates_in_first_fit_order(allocator):
	assert allocator.allocate(3) == 2

def test_throws_exception_when_no_appropriate_free_node(allocator):
	with pytest.raises(OutOfMemoryException):
		allocator.allocate(4)

def test_pops_free_list_node_upon_allocation(allocator):
	allocator.allocate(3) == 2
	assert len(allocator.free_list) == 2

def test_creates_new_node_from_remaining_memory(allocator):
	allocator.allocate(2) == 2
	free_list = allocator.free_list
	assert free_list[1].heap_index == 4
	assert free_list[1].num_bytes == 1
