from sys import argv, stdin
from memoryManager import MemoryMananager
from firstFitAllocator import FirstFitAllocator
from outOfMemoryException import OutOfMemoryException


def main():
	if len(argv) < 2:
		print('Usage: ./app.py <heap size>')
		exit(1)

	heap_size = int(argv[1])
	m = MemoryMananager(FirstFitAllocator, heap_size)

	try:
		for line in stdin:
			tokens = line.split(' ')
			if tokens[0] == 'a': # allocate
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				object_id = int(tokens[2].lstrip('O'))
				object_size = int(tokens[3].lstrip('S'))
				num_pointers = int(tokens[4].lstrip('N')) # ignoring this for now...
				class_id = int(tokens[5].lstrip('C')) # ignoring this for now...

				m.allocate(object_id, object_size)

	except OutOfMemoryException:
		pass

	finally:
		print(m.stats())
		print()


if __name__ == '__main__':
	main()
