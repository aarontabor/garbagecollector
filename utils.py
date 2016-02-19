from bisect import bisect_left


# maintains heap_index order
def add_node(free_list, node):
	i = bisect_left(free_list, node)  # performs binary-search
	free_list.insert(i, node)
	_merge_adjacent_nodes(free_list, i)

def _merge_adjacent_nodes(free_list, index):
	if index < len(free_list)-1:
		# try next node
		node = free_list[index]
		next_node = free_list[index+1]
		if node.adjacent_to(next_node):
			node.num_bytes = node.num_bytes + next_node.num_bytes
			free_list.pop(index+1)
	if index > 0:
		# try previous node
		node = free_list[index]
		prev_node = free_list[index-1]
		if node.adjacent_to(prev_node):
			prev_node.num_bytes = prev_node.num_bytes + node.num_bytes
			free_list.pop(index)
