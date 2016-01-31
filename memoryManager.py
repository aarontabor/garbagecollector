from freeListNode import FreeListNode
from heapObject import HeapObject
from freeListStatsGenerator import FreeListsStatsGenerator 


class MemoryMananager:
	def __init__(self, allocator_class, heap_size):
		self.heap_size = heap_size
		self.free_list = [FreeListNode(0, heap_size)]
		self.objects = {}
		self.allocator = allocator_class(self.free_list)

	def allocate(self, object_id, num_bytes, num_pointers):
		heap_index = self.allocator.allocate(num_bytes)
		self.objects[object_id] = HeapObject(heap_index, num_bytes, num_pointers)

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
