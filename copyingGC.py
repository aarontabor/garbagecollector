from freeListNode import FreeListNode
from copy import copy


class CopyingGC:
	def __init__(self, objects, rootset, free_list, settings):
		self.settings = settings
		self.objects = objects
		self.rootset = rootset
		self.free_list = free_list

		self.settings.heap_size = self.settings.heap_size//2 # represents size of half heap
		self.new_space = FreeListNode(0, settings.heap_size)
		self.old_space = FreeListNode(settings.heap_size, settings.heap_size)

		self.free_list.clear()
		self.free_list.append(copy(self.new_space))

		self.bytes_copied = 0

	def collect(self):
		self.copy()
		self.delete() # dead objects need to be removed from global dict
		self.swap_spaces()

	def copy(self):
		work_stack = []
		for object_id in self.rootset:
			work_stack.append(self.objects[object_id])

		current_index = self.old_space.heap_index
		while len(work_stack) > 0:
			obj = work_stack.pop()

			# copy object to old space
			obj.heap_index = current_index
			current_index = current_index + obj.size
			obj.marked = True 

			for p in obj.pointers:
				child = self.objects.get(p)
				if child != None and not child.marked:
					work_stack.append(child)

		# total bytes copied
		self.bytes_copied = current_index - self.old_space.heap_index

	def delete(self):
		toDelete = []
		for object_id, obj in self.objects.items():
			if not obj.marked:
				toDelete.append(object_id)
			else:
				obj.marked = False # clean-up for next time

		for object_id in toDelete:
			self.objects.pop(object_id)

	def swap_spaces(self):
		new_node = copy(self.old_space)
		new_node.heap_index = new_node.heap_index + self.bytes_copied
		new_node.num_bytes = new_node.num_bytes - self.bytes_copied

		self.free_list.clear()
		self.free_list.append(new_node)

		tmp = self.new_space
		self.new_space = self.old_space
		self.old_space = tmp

		self.bytes_copied = 0 # reset for next time

