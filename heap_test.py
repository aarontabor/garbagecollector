import pytest
from heap import Heap

@pytest.fixture
def heap():
	return Heap(1024)


def test_allocate_returns_heap_index(heap):
	i = heap.allocate(10)
	assert type(i) == int

def test_allocated_space_can_be_freed(heap):
	i = heap.allocate(10)
	heap.free(i, 10)

def test_free_space_cannot_be_freed(heap):
	# todo, should an exception be raised?
	pass

def test_freed_space_can_be_reused(heap):
	i1 = heap.allocate(1024)
	heap.free(i1, 1024)
	i2 = heap.allocate(10)
	assert i2 != -1
