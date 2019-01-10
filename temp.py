class A(object):
	"""docstring for A"""
	def __init__(self):
		super(A, self).__init__()
		self.a = 5

class B(A):
	"""docstring for B"""
	def __init__(self):
		super(B, self).__init__()
		self.b = 8
		


obj = A()
obj2 = B()
print(obj2.a,obj2.b)
	
class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		