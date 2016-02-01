from freeListNode import FreeListNode
from heapObject import HeapObject
from freeListStatsGenerator import FreeListsStatsGenerator 
from outOfMemoryException import OutOfMemoryException
from freeListUtils import add_node


class MemoryMananager:
	def __init__(self, allocator_class, collector_class, heap_size, high_water_percent=100, growth_factor=1.0):
		self.heap_size = heap_size
		self.high_water_percent = high_water_percent
		self.growth_factor = growth_factor

		self.free_list = [FreeListNode(0, heap_size)]
		self.objects = {}
		self.rootset = set()

		self.allocator = allocator_class(self.free_list)
		self.collector = collector_class(self.objects, self.rootset, self.free_list)

	def allocate(self, object_id, num_bytes, num_pointers, force_grow=False):
		try:
			heap_index = self.allocator.allocate(num_bytes)
			self.objects[object_id] = HeapObject(heap_index, num_bytes, num_pointers)
		except OutOfMemoryException:
			self.collect(force_grow)
			self.allocate(object_id, num_bytes, num_pointers, force_grow=True) # try again

	def collect(self, force_grow):
		s = FreeListsStatsGenerator(self.heap_size, self.free_list)
		bytes_before = s.bytes_used()
		self.collector.collect()
		bytes_after = s.bytes_used()
		print('collecting... %d %d %d' % (self.heap_size, bytes_before, bytes_after))
		if s.percent_used() >= self.high_water_percent or force_grow:
			self.grow()

	def grow(self):
		new_heap_size = self.heap_size * self.growth_factor
		heap_index = self.heap_size
		num_bytes = new_heap_size - self.heap_size
		node = FreeListNode(heap_index, num_bytes)
		add_node(self.free_list, node)
		self.heap_size = new_heap_size

	def free(self, object_id):
		o = self.objects.pop(object_id)
		self.allocator.free(o.heap_index, o.num_bytes)

	def stats(self):
		s = FreeListsStatsGenerator(self.heap_size, self.free_list)
		return '''Statistics:
	%d : objects
	%f%% : heap used
	%f : nodes in free list
	%f : average size of free list node (bytes)''' % (len(self.objects), s.percent_used(), len(self.free_list), s.average_node_size())
