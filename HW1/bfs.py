import collections
import node

def bfs(z_index_matrix, start, targets_list, threshold, no_of_columns, no_of_rows):
	visited = set(start)
	queue = collections.deque([[start]])
	shortest_target_paths = {}

	while(queue):
		path = queue.popleft()
		y,x = path[-1]
		
		if (y,x) in targets_list:
			for ele in targets_list:
				if ele == (y,x):
					shortest_target_paths[targets_list.index((y,x))] = path
					targets_list[targets_list.index((y,x))] = None
			if len([target for target in targets_list if target!=None])==0:
				return shortest_target_paths

		adjacent_node_list = node.get_adjacent_node_list(z_index_matrix, y, x, threshold, no_of_columns, no_of_rows) #return list of valid tuples/neighbours
		for adjacent_node in adjacent_node_list:
			if(adjacent_node not in visited):
				queue.append(path+[adjacent_node])
				visited.add(adjacent_node)

	return node.update_unreachable_nodes(targets_list, shortest_target_paths)