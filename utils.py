# maintains heap_index order
def add_node(free_list, node):
	i=0
	while i < len(free_list) and free_list[i].heap_index < node.heap_index:
		i = i+1
	free_list.insert(i, node)
	merge_adjacent_nodes(free_list) # over-kill, but simple

def merge_adjacent_nodes(free_list):
	i = 0
	while i+1 < len(free_list):
		node = free_list[i]
		next_node = free_list[i+1]
		if node.adjacent_to(next_node):
			node.num_bytes = node.num_bytes + next_node.num_bytes
			free_list.remove(next_node)
		else:
			i = i+1
