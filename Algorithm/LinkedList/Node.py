class Node(object):
	def __init__(self, data):
		self.data = data
		self.next = None
	
	def __repr__(self):
		return 'Node({})'.format(str(self.data))

if __name__ == '__main__':
	node = Node(1)
	print(node)
		