class HeapObject:
	def __init__(self, heap_index, size, num_pointers=1, class_id=1, thread_id=0):
		self.heap_index = heap_index
		self.size = size
		self.num_pointers = num_pointers # not using this, yet...
		self.class_id = class_id # not using this, yet...
		self.thread_id = thread_id # not using this, yet...
