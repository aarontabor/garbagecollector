import pytest
from heapObject import HeapObject


def test_assumes_sane_default_values():
	o = HeapObject(0, 16)
	assert o.num_pointers == 1
	assert o.class_id == 1
	assert o.thread_id == 0
