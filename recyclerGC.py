from freeListNode import FreeListNode
from utils import add_node


class RecyclerGC:
	def __init__(self, objects, rootset, free_list, settings):
		self.settings = settings
		self.objects = objects
		self.rootset = rootset
		self.free_list = free_list
		self.candidates = []

	def collect(self):
		# would really be maintained by write-barrier
		self.candidates = [object_id for (object_id, obj) in self.objects.items() if obj.color == 'purple']

		self.markCandidates()
		for object_id in self.candidates:
			self.scan(object_id)
		self.collectCadidates()

	def markCandidates(self):
		for object_id in self.candidates:
			obj = self.objects.get(object_id)
			self.markGrey(obj)

	def markGrey(self, obj):
		if obj.color != 'grey':
			obj.color = 'grey'
			for p in obj.pointers:
				child = self.objects.get(p)
				if child:
					child.referenceCount = child.referenceCount-1 # trial deletion
					self.markGrey(child)

	def scan(self, object_id):
		obj = self.objects.get(object_id)
		if obj.color == 'grey':
			if obj.referenceCount > 0:
				self.scanBlack(obj) # I must still be alive
			else:
				obj.color = 'white'
				for p in obj.pointers:
					child = self.objects.get(p)
					if child:
						self.scan(p)

	def scanBlack(self, obj):
		obj.color = 'black'
		for p in obj.pointers:
			child = self.objects.get(p)
			if child:
				child.referenceCount = child.referenceCount+1
				if child.color != 'black':
					self.scanBlack(child)

	def collectCadidates(self):
		while len(self.candidates) > 0:
			object_id = self.candidates.pop()
			self.collectWhite(object_id)

	def collectWhite(self, object_id):
		obj = self.objects.get(object_id)
		if object_id not in self.candidates and obj.color == 'white':
			obj.color = 'black' # avoid infinite recurse
			for p in obj.pointers:
				child = self.objects.get(p)
				if child:
					self.collectWhite(p)
			self.free(object_id)

	def free(self, object_id):
		obj = self.objects.pop(object_id)
		add_node(self.free_list, FreeListNode(obj.heap_index, obj.size))
