from freeListNode import FreeListNode
from heapObject import HeapObject
from freeListStatsGenerator import FreeListStatsGenerator 
from outOfMemoryException import OutOfMemoryException
from utils import add_node


class MemoryMananager:
	def __init__(self, allocator_class, collector_class, write_barrier_classes, settings):
		self.settings = settings
		self.free_list = [FreeListNode(0, settings.heap_size)]
		self.objects = {}
		self.rootset = set()
		self.allocator = allocator_class(self.free_list, settings)
		self.collector = collector_class(self.objects, self.rootset, self.free_list, settings)
		self.write_barriers = []
		for barrier_class in write_barrier_classes:
			self.write_barriers.append(barrier_class(self.objects, self.rootset, self.free_list, settings))
		self.stats_generator = FreeListStatsGenerator(settings, self.free_list)

	def allocate(self, object_id, num_bytes, num_pointers):
		try:
			heap_index = self.allocator.allocate(num_bytes)
		except OutOfMemoryException:
			self.collect()
			heap_index = self.allocator.allocate(num_bytes)
		self.objects[object_id] = HeapObject(heap_index, num_bytes, num_pointers)

	def collect(self):
		bytes_before = self.stats_generator.bytes_used()
		self.collector.collect()
		bytes_after = self.stats_generator.bytes_used()
		print('collecting... %d %d %d' % (self.settings.heap_size, bytes_before, bytes_after))

	def addRoot(self, object_id):
		if object_id not in self.rootset:
			for w in self.write_barriers:
				w.process(None, None, object_id)
			self.rootset.add(object_id)

	def removeRoot(self, object_id):
		if object_id in self.rootset:
			for w in self.write_barriers:
				w.process(None, object_id, None)
			self.rootset.remove(object_id)

	def writePointer(self, source_id, pointer_index, destination_id):
		source = self.objects[source_id]
		for w in self.write_barriers:
			w.process(source_id, source.pointers[pointer_index], destination_id)
		source.pointers[pointer_index] = destination_id

	def stats(self):
		return '''Statistics:
	%d : objects
	%f%% : heap used
	%f : nodes in free list
	%f : average size of free list node (bytes)''' % (len(self.objects),
			self.stats_generator.percent_used(), len(self.free_list),
			self.stats_generator.average_node_size())
