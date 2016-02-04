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
				if node.num_bytes > num_bytes:
					new_node = FreeListNode(node.heap_index+num_bytes, node.num_bytes-num_bytes)
					add_node(self.free_list, new_node)
				return node.heap_index
		raise OutOfMemoryException
