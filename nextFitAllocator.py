from freeListNode import FreeListNode
from utils import add_node
from outOfMemoryException import OutOfMemoryException


class NextFitAllocator:
	def __init__(self, free_list, settings):
		self.free_list = free_list
		self.current_index = 0

	def allocate(self, num_bytes):
		for i in range(len(self.free_list)):
			index = (self.current_index+i) % len(self.free_list)
			node = self.free_list[index]
			if node.num_bytes >= num_bytes:
				self.free_list.pop(index)
				if node.num_bytes > num_bytes:
					new_node = FreeListNode(node.heap_index+num_bytes, node.num_bytes-num_bytes)
					add_node(self.free_list, new_node)
				self.current_index = index
				return node.heap_index
		raise OutOfMemoryException
