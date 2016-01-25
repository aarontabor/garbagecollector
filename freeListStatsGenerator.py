class FreeListsStatsGenerator():
	def __init__(self, heap_size, free_list):
		self.heap_size = heap_size
		self.free_list = free_list

	def percent_free(self):
		return self.bytes_free()/self.heap_size * 100

	def percent_used(self):
			return self.bytes_used()/self.heap_size * 100

	def average_node_size(self):
		l = len(self.free_list)
		if l == 0:
			return 0
		else:
			return self.bytes_free() / l

	def bytes_free(self):
		return sum([n.num_bytes for n in self.free_list])

	def bytes_used(self):
		return self.heap_size - self.bytes_free()
