import pytest
from heapObject import HeapObject
from referenceCountingWriteBarrier import ReferenceCountingWriteBarrier


class MockSettings:
	pass

@pytest.fixture
def settings():
	return MockSettings()


def test_reference_counts_are_maintained(settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(8, 8)
	o3 = HeapObject(16, 8)

	o1.pointers[0] = 2

	# extra pointers are coming from outside the context of example
	o1.referenceCount = 1
	o2.referenceCount = 2
	o3.referenceCount = 1

	objects = {1: o1, 2: o2, 3: o3}
	rootset = set()
	free_list = []

	write_barrier = ReferenceCountingWriteBarrier(objects, rootset, free_list, settings)

	write_barrier.process(1, 2, 3) # o1 changes pointer from o2 to o3

	assert o2.referenceCount == 1
	assert o3.referenceCount == 2

def test_reference_count_write_from_none(settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(8, 8)

	o1.pointers[0] = None

	# extra pointers are coming from outside the context of example
	o1.referenceCount = 1
	o2.referenceCount = 1

	objects = {1: o1, 2: o2}
	rootset = set()
	free_list = []

	write_barrier = ReferenceCountingWriteBarrier(objects, rootset, free_list, settings)

	write_barrier.process(1, None, 2) # o1 changes pointer from None to o2

	assert o2.referenceCount == 2

def test_reference_count_write_to_none(settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(8, 8)

	o1.pointers[0] = o2

	# extra pointers are coming from outside the context of example
	o1.referenceCount = 1
	o2.referenceCount = 2

	objects = {1: o1, 2: o2}
	rootset = set()
	free_list = []

	write_barrier = ReferenceCountingWriteBarrier(objects, rootset, free_list, settings)

	write_barrier.process(1, 2, None) # o1 changes pointer from o2 to None

	assert o2.referenceCount == 1

def test_frees_objects_with_zero_reference_count(settings):
	o1 = HeapObject(0, 8)
	o2 = HeapObject(10, 8)
	o3 = HeapObject(20, 8)

	o1.pointers[0] = 2
	o2.pointers[0] = 3

	# pointer to o1 comes from outside context of example
	o1.referenceCount = 1
	o2.referenceCount = 1
	o3.referenceCount = 1

	objects = {1: o1, 2: o2, 3: o3}
	rootset = set()
	free_list = []

	write_barrier = ReferenceCountingWriteBarrier(objects, rootset, free_list, settings)
	write_barrier.process(1, 2, None)

	live_objects = objects.items()

	assert o2 not in live_objects
	assert o3 not in live_objects

	assert len(free_list) == 2
	assert free_list[0].heap_index == 10
	assert free_list[1].heap_index == 20
