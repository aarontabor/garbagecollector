from sys import argv, stdin
from memoryManager import MemoryMananager
from firstFitAllocator import FirstFitAllocator
from markSweepGC import MarkSweepGC
from outOfMemoryException import OutOfMemoryException


def main():
	if len(argv) < 2:
		print('Usage: ./app.py <heap size>')
		exit(1)

	heap_size = int(argv[1])
	m = MemoryMananager(FirstFitAllocator, MarkSweepGC, heap_size)

	try:
		for line in stdin:
			tokens = line.split(' ')
			if tokens[0] == 'a': # allocate
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				object_id = int(tokens[2].lstrip('O'))
				object_size = int(tokens[3].lstrip('S'))
				num_pointers = int(tokens[4].lstrip('N'))
				class_id = int(tokens[5].lstrip('C')) # ignoring this for now...

				m.allocate(object_id, object_size, num_pointers)

			if tokens[0] == 'w': # write pointer
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				parent_id = int(tokens[2].lstrip('P'))
				pointer_index = int(tokens[3].lstrip('#'))
				object_id = int(tokens[4].lstrip('O'))

				m.objects[parent_id].pointers[pointer_index] = object_id

			if tokens[0] == '+': # add to rootset
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				object_id = int(tokens[2].lstrip('O'))

				m.rootset.add(object_id)

			if tokens[0] == '-': # remove from rootset
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				object_id = int(tokens[2].lstrip('O'))

				m.rootset.remove(object_id)

	except OutOfMemoryException:
		print('Out of memory...')

	finally:
		print(m.stats())
		print()


if __name__ == '__main__':
	main()
