import heapq
import node

def find_cost_from_parent_to_child(parent_cordinate): 
	(y,x) = parent_cordinate
	return {(y,x-1):10,(y+1,x):10,(y,x+1):10,(y-1,x):10,(y-1,x-1):14,(y+1,x-1):14,(y+1,x+1):14,(y-1,x+1):14}
	
def ucs(z_index_matrix, start, targets_list, threshold, no_of_columns, no_of_rows):
	open=[]
	heapq.heappush(open,(0,[start]))
	deleted={}
	open_dict={start:0}
	closed={}
	shortest_target_paths = {}

	while open:
		(path_cost, path) = heapq.heappop(open)
		(y,x) = path[-1]

		if (y,x) in deleted and deleted[(y,x)] == path_cost:
			deleted.pop((y,x),None)
			continue

		open_dict.pop((y,x),None)

		if (y,x) in targets_list:
			for ele in targets_list:
				if ele == (y,x):
					shortest_target_paths[targets_list.index((y,x))] = path
					targets_list[targets_list.index((y,x))] = None
			if len([target for target in targets_list if target!=None])==0:
				return shortest_target_paths

		adjacent_node_list = [(y-1,x-1),(y,x-1),(y+1,x-1),(y+1,x),(y+1,x+1),(y,x+1),(y-1,x+1),(y-1,x)]
		parent_child_cost_map = find_cost_from_parent_to_child((y,x))

		for adjacent_node in adjacent_node_list:
			y1 = adjacent_node[0]
			x1 = adjacent_node[1]
			if (0<=y1<no_of_columns and 0<=x1<no_of_rows and abs(z_index_matrix[x][y]-z_index_matrix[x1][y1])<=threshold):
				path_cost_of_child = path_cost + parent_child_cost_map[adjacent_node]
	
				is_child_in_open = adjacent_node in open_dict
				is_child_in_closed = adjacent_node in closed
	
				if (not is_child_in_open and not is_child_in_closed):
					heapq.heappush(open,(path_cost_of_child, path + [adjacent_node]))
					open_dict[adjacent_node] = path_cost_of_child
	
				elif is_child_in_open:
					if (path_cost_of_child < open_dict[adjacent_node]):
						deleted[adjacent_node] = open_dict[adjacent_node]
						heapq.heappush(open, (path_cost_of_child, path + [adjacent_node]))
						open_dict[adjacent_node] = path_cost_of_child
	
				elif is_child_in_closed:
					if (path_cost_of_child < closed[adjacent_node]):
						del closed[adjacent_node]
						heapq.heappush(open, (path_cost_of_child, path + [adjacent_node]))
						open_dict[adjacent_node] = path_cost_of_child

		closed[(y,x)]=path_cost

	return node.update_unreachable_nodes(targets_list, shortest_target_paths)
