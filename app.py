from sys import stdin
from argparse import ArgumentParser
from memoryManager import MemoryMananager
from firstFitAllocator import FirstFitAllocator
from markSweepGrowGC import MarkSweepGrowGC
from copyingGC import CopyingGC
from nullGC import NullGC
from referenceCountingWriteBarrier import ReferenceCountingWriteBarrier
from outOfMemoryException import OutOfMemoryException


def main():
	parser = ArgumentParser()
	parser.add_argument('--heap_size', type=int, default=1)
	parser.add_argument('--high_water_percent', type=int, default=100)
	parser.add_argument('--growth_factor', type=float, default=1.0)
	parser.add_argument('--write_barrier', type=str, default='')
	parser.add_argument('collector', type=str)
	settings = parser.parse_args()

	collector_class = parseCollectorClass(settings.collector)
	write_barrier_classes = parseWriteBarrierClasses(settings.write_barrier)

	m = MemoryMananager(FirstFitAllocator, collector_class, write_barrier_classes, settings)

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

				m.writePointer(parent_id, pointer_index, object_id)

			if tokens[0] == '+': # add to rootset
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				object_id = int(tokens[2].lstrip('O'))

				m.addRoot(object_id)

			if tokens[0] == '-': # remove from rootset
				thread_id = int(tokens[1].lstrip('T')) # ignoring this for now...
				object_id = int(tokens[2].lstrip('O'))

				m.removeRoot(object_id)

	except OutOfMemoryException:
		print('Out of memory...')

	print(m.stats())


def parseCollectorClass(collector_name):
	collector_class = None
	if collector_name == 'mark_sweep_grow':
		collector_class = MarkSweepGrowGC
	elif collector_name == 'copying':
		collector_class = CopyingGC
	elif collector_name == 'null_gc':
		collector_class = NullGC

	if collector_class == None:
		raise InvalidCollectorName

	return collector_class
	
def parseWriteBarrierClasses(write_barrier_name):
	write_barrier_classes = []
	if write_barrier_name == 'reference_counting':
		write_barrier_classes.append(ReferenceCountingWriteBarrier)

	return write_barrier_classes


if __name__ == '__main__':
	main()
