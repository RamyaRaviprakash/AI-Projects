import re
import collections
import bfs
import ucs
import astar

def main():
	with open("input.txt") as f:
		algo = f.readline().strip("\n").lstrip(" ").rstrip(" ")

		sec_line = f.readline().strip("\n").lstrip(" ").rstrip(" ").split(" ")
		no_of_columns = int(sec_line[0])
		no_of_rows = int(sec_line[1])
		
		third_line = f.readline().strip("\n").lstrip(" ").rstrip(" ").split(" ")
		landing_col = int(third_line[0])
		landing_row = int(third_line[1])
		
		threshold = int(f.readline().strip("\n").lstrip(" ").rstrip(" "))

		no_of_targets = int(f.readline().strip("\n").lstrip(" ").rstrip(" "))

		targets_list = [tuple(map(int, f.readline().strip("\n").lstrip(" ").rstrip(" ").split(" "))) for target in range(no_of_targets)]

		z_index_matrix = [list(map(int,re.sub(" +", " ", f.readline().strip("\n").lstrip(" ").rstrip(" ")).split(" "))) for rows in range(no_of_rows)]

		if algo == "BFS":
			shortest_target_paths = bfs.bfs(z_index_matrix, (landing_col,landing_row), targets_list, threshold, no_of_columns, no_of_rows)
		elif algo == "UCS":
			shortest_target_paths = ucs.ucs(z_index_matrix, (landing_col,landing_row), targets_list, threshold, no_of_columns, no_of_rows)
		elif algo == "A*":
			shortest_target_paths = {}
			index = 0
			for target in targets_list:
				shortest_target_path = astar.astar(z_index_matrix, (landing_col,landing_row), [target], threshold, no_of_columns, no_of_rows)
				shortest_target_paths[index] = shortest_target_path[0]
				index += 1

		write_to_output(shortest_target_paths)

def write_to_output(shortest_target_paths):
	with open("output.txt","w") as f:
		output_str=""
		for key in sorted(shortest_target_paths.keys()):
			path = shortest_target_paths[key]
			if path:
				output_str+=" ".join([",".join(map(str,cordinate)) for cordinate in path])+"\n"
			else:
				output_str+="FAIL\n"
		output_str = output_str.rstrip("\n")
		f.write(output_str)	

if __name__=="__main__":
	main()