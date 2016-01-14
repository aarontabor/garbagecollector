from freeList import FreeList
from freeListNode import FreeListNode
from freeListStatsGenerator import FreeListsStatsGenerator


class Heap:
	def __init__(self, heap_size):
		initial_node = FreeListNode(0, heap_size)
		self.free_list = FreeList([initial_node])
		self.data = bytearray(heap_size) # don't actually need this yet...

	def allocate(self, num_bytes):
		node = self.free_list.pop_node(num_bytes)
		if node:
			bytes_remaining = node.num_bytes - num_bytes
			if bytes_remaining:
				new_index = node.heap_index + num_bytes
				new_node = FreeListNode(new_index, bytes_remaining)
				self.free_list.add_node(new_node)
			return node.heap_index
		else:
			return -1

	def free(self, heap_index, num_bytes):
		new_node = FreeListNode(heap_index, num_bytes)
		self.free_list.add_node(new_node)

	def stats(self):
		s = FreeListsStatsGenerator(self.size(), self.free_list)
		print(
'''Heap Statistics:
	%f%% : heap used
	%f : nodes in free list
	%f : average size of free list node (bytes)''' % (s.percent_used(), len(self.free_list), s.average_node_size()))

	def size(self):
		return len(self.data)
