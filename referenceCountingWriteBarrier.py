from utils import add_node
from freeListNode import FreeListNode


class ReferenceCountingWriteBarrier:
	def __init__(self, objects, rootset, free_list, settings):
		self.objects = objects
		self.rootset = rootset
		self.free_list = free_list
		self.settings = settings

	def process(self, source_id, old_destination_id, new_destination_id):
		old_object = self.objects.get(old_destination_id)
		new_object = self.objects.get(new_destination_id)

		if new_object:
			new_object.referenceCount = new_object.referenceCount+1

		if old_object:
			old_object.referenceCount = old_object.referenceCount-1
			if old_object.referenceCount == 0:
				self.free(old_destination_id)

	def free(self, object_id):
		obj = self.objects.pop(object_id)
		add_node(self.free_list, FreeListNode(obj.heap_index, obj.size))
		for p in obj.pointers:
			child = self.objects.get(p)
			if child:
				child.referenceCount = child.referenceCount-1
				if child.referenceCount == 0:
					self.free(p)
