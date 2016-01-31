from freeListNode import FreeListNode
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
		i=0
		while i < len(self.free_list) and self.free_list[i].heap_index < heap_index:
			i = i+1
		self.free_list.insert(i, FreeListNode(heap_index, num_bytes))
		self.merge_adjacent_nodes() # over-kill, but simple

	def merge_adjacent_nodes(self):
		i = 0
		while i+1 < len(self.free_list):
			node = self.free_list[i]
			next_node = self.free_list[i+1]
			if node.adjacent_to(next_node):
				node.num_bytes = node.num_bytes + next_node.num_bytes
				self.free_list.remove(next_node)
			else:
				i = i+1
