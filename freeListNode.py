class FreeListNode:
	def __init__(self, heap_index, num_bytes):
		self.heap_index = heap_index
		self.num_bytes = num_bytes

	def adjacent_to(self, node):
		if self.heap_index+self.num_bytes == node.heap_index:
			return True
		elif node.heap_index+node.num_bytes == self.heap_index:
			return True
		else:
			return False

	def __repr__(self):
		return "<%d, %d>" % (self.heap_index, self.num_bytes)

	def __lt__(self, other):
		return self.heap_index < other.heap_index

	def __eq__(self, other):
		return self.heap_index == other.heap_index
