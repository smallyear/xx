from Node import Node
class UnorderedList():
	def __init__(self):
		self.head = None

	def __repr__(self):
		current =  self.head
		liststr = ''
		while current != None:
			liststr = liststr  + str(current) + '->'
			current = current.next
		return liststr + 'None'

	def isEmpty(self):
		return self.head == None

	def size(self):
		current =  self.head
		num = 0
		while current != None:
			num += 1
			current = current.next	
		return num
	def add(self,item):
		node = Node(item)
		node.next = self.head
		self.head = node

	def remove(self,item):
		previous = None
		current = self.head
		found = False
		while not found:
			data = current.data
			if data == item:
				found = True
			else:
				previous = current
				current = current.next
		if previous == None:
			self.head = current.next
		else:
			previous.next = current.next
	def search(self,item):
		current = self.head
		while  current != None:
			data = current.data
			if data == item:
				return True
			current = current.next
		return False
	def append(self,item):
		current = self.head
		appendNode = Node(item)
		while current != None:
			if current.next == None:
				current.next = appendNode
				current = appendNode.next
			else:
				current = current.next
	def index(self,item):
		current = self.head
		num = 0
		while current != None:
			if current.data == item:
				return num
			else:
				num += 1
				current = current.next
	def insert(self,pos,item):
		previous = None
		insertNode = Node(item)
		current = self.head
		num = 0
		while current != None:
			if pos == 0:
				self.head = insertNode
				insertNode.next = current
				return
			else:
				if num == pos:
					previous.next = insertNode
					insertNode.next = current
					return 
				else:
					num += 1
					previous = current
					current = current.next
	def pop(self,index=0):
		current = self.head
		if index == 0:
			self.remove(current.data)
			return current
		else:
			num = 0
			while current != None:
				if index == num:
					self.remove(current.data)
					return current
				else:
					num += 1
					current = current.next

if __name__ == '__main__':
	unorderedlist = UnorderedList()
	unorderedlist.add('1')
	unorderedlist.add('2')
	unorderedlist.add('3')
	unorderedlist.add('4')
	unorderedlist.add('5')
	print(unorderedlist)
	print(unorderedlist.size())
	unorderedlist.remove('2')
	print(unorderedlist)
	unorderedlist.remove('1')
	print(unorderedlist)
	print(unorderedlist.search('1'))
	print(unorderedlist.search('2'))
	unorderedlist.append('2')
	unorderedlist.append('1')
	print(unorderedlist)
	print(unorderedlist.index('5'))
	unorderedlist.insert(1,'7')
	unorderedlist.insert(1,'8')
	unorderedlist.insert(4,'9')
	print(unorderedlist)
	print(unorderedlist.pop())
	print(unorderedlist)
	print(unorderedlist.pop(2))
	print(unorderedlist)
