import sys

level_dict = {}
level_count = 0
level_record = {}
data_click = {}
class Node:
	def __init__(self,val):
		self.val = val
		self.left = None
		self.right = None

class Tree:
	def __init__(self):
		self.root = None
	def getRoot(self):
		return self.root
	# Add root into the tree
	def add(self,val):
		if self.root is None:
			self.root = Node(val)
		else:
			self.add_child(val,self.root)
	# Adding child for the root node
	def add_child(self,val,node):
		if val < node.val:
			if node.left is not None:
				self.add_child(val,node.left)
			else:
				node.left = Node(val)
		else:
			if node.right is not None:
				self.add_child(val,node.right)
			else:
				node.right = Node(val)
	# getting the nodes of data level by level
	def level_order_traversal(self, queue,depth):
		queue_new = []
		data = []
		if not queue:
			return
		else:
			global data_click
			for node in queue:
				temp_dict = {}
				data.append(node.val)
				if node.left is not None:
					queue_new.append(node.left)
					temp_dict['left'] = node.left.val
				else:
					temp_dict['left'] = None
				if node.right is not None:
					temp_dict['right'] = node.right.val
					queue_new.append(node.right)
				else:
					temp_dict['right'] = None
				data_click[node.val] = temp_dict
			global level_dict
			global level_count
			if level_count not in level_dict:
				level_dict[level_count] = data
				level_count += 1
		self.level_order_traversal(queue_new,depth)
	# Getting the Depth(height) of the tree
	def max_depth(self, this_node):
		if this_node is None:
			return 0
		left_subtree = self.max_depth(this_node.left)
		right_subtree = self.max_depth(this_node.right)
		return 1 + max(left_subtree, right_subtree)
	# children which are supposed to be in each level.for ex: level=3,no of child= 2^3=>8
	def level_nodes_count(self,level):
		return pow(2,level)
	# for giving space for the data's based on depth and level
	def space_count_nodes(self,depth,level):
		return pow(2,(depth-level))
	# getting a child node from the parent
	def childrenForParent(self,parent_data):
		children_list = []
		if parent_data is not None:
			temp_par_dict = data_click[parent_data]
			children_list.append(temp_par_dict['left'])
			children_list.append(temp_par_dict['right'])
		else:
			children_list.append(None)
			children_list.append(None)
		return children_list
	# getting a list -> contains the number of data's which are supposed to be in the level
	def get_node_list(self,depth,level,list_data):
		list_nodes = []
		global level_record
		if level == 0:
			list_nodes.append(self.root.val)
			return list_nodes	
		if level in level_record:
			parent_list = level_record[level-1]
			for parent in parent_list:
				list_nodes.extend(self.childrenForParent(parent))
			return list_nodes
	# prividing the string which is to be print into the output file 
	def give_tree(self,level,level_data):
		string_to_print = ""
		space_count = 0
		data_from_level = level_record[level]
		for i in range(0,len(data_from_level)):
			if i != 0:
				space_count = 2*self.space_count_nodes(depth,level)
			else:
				space_count = self.space_count_nodes(depth,level)
			string_to_print += ' '*space_count
			if data_from_level[i] is None:
				string_to_print += ' '
			else:
				string_to_print += str(data_from_level[i])
		return string_to_print					
	# For writting the tree structure
	def print_treeStructure(self,depth,output_file):
		with open(output_file, "w") as text_file:
			for i in range(0,depth):
				level_record[i] = []
			for level,list_data in level_dict.items():
				level_record[level] = self.get_node_list(depth,level,list_data)
				tree_data = self.give_tree(level,level_record[level])
				text_file.write(tree_data)
				text_file.write('\n')
				text_file.write('\n')

# Reading an input file
def read_file(file_name):
	ip_file = open(file_name,'r')
	ip_list = []
	while True:
		data = ip_file.readline()
		if not data:
			break
		ip_list.append(data.strip())
	return ip_list


if __name__ == '__main__':
	input_file = str(input('Enter the input file name: '))
	output_file_name = str(input('Enter the input file name: '))
	data_list = read_file(input_file)
	tree = Tree()
	data_list_int = []
	for i in range(0,len(data_list)):
		data = int(data_list[i])
		if data not in data_list_int:
			data_list_int.append(data)
	for i in range(0,len(data_list_int)):
		tree.add(data_list_int[i])
	depth = tree.max_depth(tree.root)
	tree.level_order_traversal([tree.getRoot()],depth)
	tree.print_treeStructure(depth,output_file_name)

		