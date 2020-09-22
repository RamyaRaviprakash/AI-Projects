
def get_adjacent_node_list(z_index_matrix,y,x, threshold, no_of_columns, no_of_rows):
	possible_adjacent_nodes = [(y-1,x-1),(y,x-1),(y+1,x-1),(y+1,x),(y+1,x+1),(y,x+1),(y-1,x+1),(y-1,x)]
	filtered_adjacent_nodes = []
	for y1,x1 in possible_adjacent_nodes:
		if (0<=y1<no_of_columns and 0<=x1<no_of_rows and abs(z_index_matrix[x][y]-z_index_matrix[x1][y1])<=threshold):
			filtered_adjacent_nodes.append((y1,x1))
	return filtered_adjacent_nodes

def update_unreachable_nodes(targets_list, shortest_target_paths):
	for target in targets_list:
		if target!=None:
			shortest_target_paths[targets_list.index(target)] = None
	return shortest_target_paths
