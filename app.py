from sys import argv, stdin
from heap import Heap, OutOfMemoryException
from heapObject import HeapObject


def main():
	if len(argv) < 2:
		print('Usage: ./app.py <heap size>')
		exit(1)

	heap = Heap(int(argv[1]))
	objects = {} # object_id -> HeapObject

	try:
		for line in stdin:
			tokens = line.split(' ')
			if tokens[0] == 'a': # allocate
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				object_id = int(tokens[2].lstrip('O'))
				object_size = int(tokens[3].lstrip('S'))
				num_pointers = int(tokens[4].lstrip('N')) # ignoring this for now...
				class_id = int(tokens[5].lstrip('C')) # ignoring this for now...

				heap_index = heap.allocate(object_size)
				objects[object_id] = HeapObject(heap_index, object_size)

	except OutOfMemoryException:
		pass

	finally:
		print('%d objects alive at program termination.' % len(objects))
		heap.stats()
		print()


if __name__ == '__main__':
	main()
