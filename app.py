from sys import argv, stdin
from heap import Heap, OutOfMemoryException


class Obj: # data-object to store object info
	def __init__(self, addr, size):
		self.addr = addr
		self.size = size


def main():
	if len(argv) < 2:
		print('Usage: ./app.py <heap size>')
		exit(1)

	heap = Heap(int(argv[1]))
	objects = {} # object_id -> Obj

	try:
		for line in stdin:
			tokens = line.split(' ')
			if tokens[0] == 'a': # allocate
				object_id = int(tokens[1])
				object_size = int(tokens[2])
				i = heap.allocate(object_size)
				objects[object_id] = Obj(i, object_size)

			elif tokens[0] == 'f': # free
				object_id = int(tokens[1])
				o = objects[object_id]
				objects.pop(object_id)
				heap.free(o.addr, o.size)

			elif tokens[0] == 'e': # end
				break

			else: # something went wrong
				print('Error: could not parse tracefile line:\n\t%s' % line)
				break

	except OutOfMemoryException:
		pass

	finally:
		print('%d objects alive at program termination.' % len(objects))
		heap.stats()
		print()


if __name__ == '__main__':
	main()
