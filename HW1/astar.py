import heapq
import node

def find_cost_from_parent_to_child(parent_cordinate): 
	(y,x) = parent_cordinate
	return {(y,x-1):10,(y+1,x):10,(y,x+1):10,(y-1,x):10,(y-1,x-1):14,(y+1,x-1):14,(y+1,x+1):14,(y-1,x+1):14}
	
def find_estimated_path_cost_from_child_to_target(child_cordinate, target_cordinate): #heuristic function
	child_x, child_y = child_cordinate
	target_x, target_y = target_cordinate
	D = 10
	D2 = 14
	dx = abs(target_x-child_x)
	dy = abs(target_y-child_y)
	return D*(dx+dy)+((D2-(2*D))*min(dx,dy))

def find_elevation_diff(z_index_matrix, parent_cordinate, child_cordinate):
	parent_cordinate_y = parent_cordinate[0]
	parent_cordinate_x = parent_cordinate[1]
	child_cordinate_y = child_cordinate[0]
	child_cordinate_x = child_cordinate[1]
	return abs(z_index_matrix[parent_cordinate_x][parent_cordinate_y]-z_index_matrix[child_cordinate_x][child_cordinate_y])

# targets_list will always contain one element
def astar(z_index_matrix, start, targets_list, threshold, no_of_columns, no_of_rows):
	open=[]
	heapq.heappush(open,(0,0,[start]))
	deleted={}
	open_dict={start:0}
	closed={}
	shortest_target_paths = {} # key: index of target in target_list, value: path of target, so that output is printed in order of input targets

	while open:
		(estimated_total_cost, path_cost, path) = heapq.heappop(open)
		(y,x) = path[-1]

		if (y,x) in deleted and deleted[(y,x)] == estimated_total_cost:
			deleted.pop((y,x),None)
			continue

		open_dict.pop((y,x),None)

		if (y,x) in targets_list:
			shortest_target_paths[targets_list.index((y,x))] = path
			targets_list[targets_list.index((y,x))] = None
			if len([target for target in targets_list if target!=None])==0: # can be optimized using target_list as a dict
				return shortest_target_paths

		adjacent_node_list = node.get_adjacent_node_list(z_index_matrix, y, x, threshold, no_of_columns, no_of_rows) #return list of valid tuples/neighbours
		parent_child_cost_map = find_cost_from_parent_to_child((y,x))

		for adjacent_node in adjacent_node_list:
			path_cost_of_child = path_cost + parent_child_cost_map[adjacent_node] + find_elevation_diff(z_index_matrix, (y,x), adjacent_node) #g(n) 
			path_cost_from_child_to_target = find_estimated_path_cost_from_child_to_target(adjacent_node, targets_list[0]) #h(n)
			total_cost = path_cost_of_child + path_cost_from_child_to_target #f(n)

			is_child_in_open = adjacent_node in open_dict
			is_child_in_closed = adjacent_node in closed

			if (not is_child_in_open and not is_child_in_closed):
				heapq.heappush(open,(total_cost, path_cost_of_child, path + [adjacent_node])) # (f,g,[path])
				open_dict[adjacent_node] = total_cost

			elif is_child_in_open:
				if (total_cost < open_dict[adjacent_node]):
					deleted[adjacent_node] = open_dict[adjacent_node]
					heapq.heappush(open, (total_cost, path_cost_of_child, path + [adjacent_node]))
					open_dict[adjacent_node] = total_cost

			elif is_child_in_closed:
				if (total_cost < closed[adjacent_node]):
					del closed[adjacent_node]
					heapq.heappush(open, (total_cost, path_cost_of_child, path + [adjacent_node]))
					open_dict[adjacent_node] = total_cost

		closed[(y,x)]=estimated_total_cost

	return node.update_unreachable_nodes(targets_list, shortest_target_paths)

