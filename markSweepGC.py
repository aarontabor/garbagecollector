from utils import add_node
from freeListNode import FreeListNode


class MarkSweepGC:
	def __init__(self, objects, rootset, free_list, settings):
		self.settings = settings
		self.objects = objects
		self.rootset = rootset
		self.free_list = free_list

	def collect(self):
		self.mark()
		self.sweep()

	def mark(self):
		work_stack = []
		for object_id in self.rootset:
			work_stack.append(self.objects[object_id])

		while len(work_stack) > 0:
			obj = work_stack.pop()
			obj.marked = True
			for p in obj.pointers:
				child = self.objects.get(p)
				if child != None and not child.marked:
					work_stack.append(child)

	def sweep(self):
		toDelete = []
		for object_id, obj in self.objects.items():
			if not obj.marked:
				add_node(self.free_list, FreeListNode(obj.heap_index, obj.size))
				toDelete.append(object_id)
			else:
				obj.marked = False # clean-up for next time

		for object_id in toDelete:
			self.objects.pop(object_id)
