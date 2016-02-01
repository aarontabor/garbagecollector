from freeListNode import FreeListNode
from freeListUtils import add_node
from outOfMemoryException import OutOfMemoryException


class FirstFitAllocator:
	def __init__(self, free_list):
		self.free_list = free_list

	def allocate(self, num_bytes):
		for node in self.free_list:
			if node.num_bytes >= num_bytes:
				self.free_list.remove(node)
				self.free(node.heap_index+num_bytes, node.num_bytes-num_bytes)
				return node.heap_index
		raise OutOfMemoryException

	def free(self, heap_index, num_bytes):
		add_node(self.free_list, FreeListNode(heap_index, num_bytes))

