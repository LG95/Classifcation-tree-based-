class Node:
	def __init__(self, label, test = None):
		self.test = test
		self.label = label

		if self.test is not None:
			self.children = []
			self.branches = []

	def __str__(self):
		def recurse(node, level):
			s = '| ' * level + str(node.label) + '\n'

			if node.test is not None:
				for child, branch in zip(node.children, node.branches):
					s += '| ' * level + str(branch) + '\n'
					s += recurse(child, level + 1)

			return s

		return recurse(self, 0)

	def add_branch(self, value):
		self.branches.append(value)

	def add_child(self, child):
		self.children.append(child)

	def classify(self, record):
		current = self

		while current.test is not None:
			for branch, child in zip(current.branches, current.children):
				if current.test(record) == branch:
					current = child
					break

		return current.label