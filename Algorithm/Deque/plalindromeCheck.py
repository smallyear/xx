from Deque import Deque
def plalindromeCheck(str):
	deque = Deque()
	for i in str:
		deque.addFront(i)

	flag = True
	while flag:
		if deque.size() > 1:
			front = deque.removeFront()
			rear = deque.removeRear()
			if front != rear:
				return False
		else:
			flag = False
	return True

if __name__ == '__main__':
	str = 'miami'
	print(plalindromeCheck(str))
	str = 'imami'
	print(plalindromeCheck(str))
	str = 'abccba'
	print(plalindromeCheck(str))


