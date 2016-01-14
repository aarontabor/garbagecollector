import pytest
from freeListNode import FreeListNode

@pytest.fixture
def node():
	return FreeListNode(2,1)


def test_adjacent_node_before(node):
	n = FreeListNode(1,1)
	assert node.adjacent_to(n)

def test_adjacent_node_after(node):
	n = FreeListNode(3,1)
	assert node.adjacent_to(n)

def test_unadjacent_node_before(node):
	n = FreeListNode(0,1)
	assert not node.adjacent_to(n)

def test_unadjacent_node_after(node):
	n = FreeListNode(4,1)
	assert not node.adjacent_to(n)
