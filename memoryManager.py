from freeListNode import FreeListNode
from heapObject import HeapObject
from freeListStatsGenerator import FreeListsStatsGenerator 
from outOfMemoryException import OutOfMemoryException
from utils import add_node


class MemoryMananager:
	def __init__(self, allocator_class, collector_class, settings):
		self.settings = settings
		self.free_list = [FreeListNode(0, settings.heap_size)]
		self.objects = {}
		self.rootset = set()
		self.allocator = allocator_class(self.free_list, settings)
		self.collector = collector_class(self.objects, self.rootset, self.free_list, settings)

	def allocate(self, object_id, num_bytes, num_pointers):
		try:
			heap_index = self.allocator.allocate(num_bytes)
		except OutOfMemoryException:
			self.collect()
			heap_index = self.allocator.allocate(num_bytes)
		self.objects[object_id] = HeapObject(heap_index, num_bytes, num_pointers)

	def collect(self):
		s = FreeListsStatsGenerator(self.settings.heap_size, self.free_list)
		bytes_before = s.bytes_used()
		self.collector.collect()
		bytes_after = s.bytes_used()
		print('collecting... %d %d %d' % (self.settings.heap_size, bytes_before, bytes_after))

	def stats(self):
		s = FreeListsStatsGenerator(self.settings.heap_size, self.free_list)
		return '''Statistics:
	%d : objects
	%f%% : heap used
	%f : nodes in free list
	%f : average size of free list node (bytes)''' % (len(self.objects), s.percent_used(), len(self.free_list), s.average_node_size())
