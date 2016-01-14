class FreeList(list):
	def __init__(self, initial_list=[]):
		super().__init__(initial_list)

	def add_node(self, new_node):
		found = False
		for (i, node) in enumerate(self):
			if node.heap_index > new_node.heap_index:
				self.insert(i, new_node)
				found = True
				break
		if not found:
			self.append(new_node)
		self.merge_adjacent_nodes() # over-kill, but simple

	def merge_adjacent_nodes(self):
		i = 0
		while i+1 < len(self):
			node = self[i]
			next_node = self[i+1]
			if node.adjacent_to(next_node):
				node.num_bytes = node.num_bytes + next_node.num_bytes
				self.remove(next_node)
			else:
				i = i+1

	def pop_node(self, num_bytes):
		for node in self:
			if node.num_bytes >= num_bytes:
				self.remove(node)
				return node
		return None
