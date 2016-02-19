from freeListNode import FreeListNode
from utils import add_node
from outOfMemoryException import OutOfMemoryException


class FirstFitAllocator:
	def __init__(self, free_list, settings):
		# So far, I don't really need settings, other allocators may...
		self.free_list = free_list

	def allocate(self, num_bytes):
		for index, node in enumerate(self.free_list):
			if node.num_bytes >= num_bytes:
				self.free_list.pop(index)
				if node.num_bytes > num_bytes:
					new_node = FreeListNode(node.heap_index+num_bytes, node.num_bytes-num_bytes)

					# target for future optimization, I know exactly where it goes
					add_node(self.free_list, new_node)
				return node.heap_index
		raise OutOfMemoryException
