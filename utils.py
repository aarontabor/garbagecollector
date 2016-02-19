# maintains heap_index order
def add_node(free_list, node):
	i=0
	while i < len(free_list) and free_list[i].heap_index < node.heap_index:
		i = i+1
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
