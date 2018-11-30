### 单例模式
#### 1.使用__new__方法
```python
class Singleton(object):
	def __new__(cls,*args,**kwargs):
		if not hasattr(cls,'_instance'):
			cls._instance = super(Singleton,cls).__new__(cls,*args,**kwargs)
		return cls._instance

class Myclass(Singleton):
	def __init(self):
		pass
```
#### 2.import 方法
作为python的模块天生是单例模式,因为模块在第一次导入时，会生成 .pyc 文件，当第二次导入时，就会直接加载 .pyc 文件，而不会再次执行模块代码。因此，我们只需把相关的函数和数据定义在一个模块中，就可以获得一个单例对象了
```python
#Singleton.py
class Singleton(object):
	def __init__(self):
		pass
	def foo(self):
		pass
singleton = Singleton()

#some file to use
from Singleton import singleton

singleton.foo()
```
#### 3.共享属性
创建实例时把所有实例的__dict__指向同一个字典,这样它们具有相同的属性和方法.
```python
class Singleton(object):
	_state = {}
	def __new__(self, *args,**kwargs):
		ob = super(Singleton, cls).__new__(cls,*args,**kwargs)
		ob.__dict__ = cls._state
		return ob

class Myclass(Singleton):
	pass
		
```
#### 4.装饰器模式
定义了一个装饰器 singleton，它返回了一个内部函数 getinstance，该函数会判断某个类是否在字典 instances 中，如果不存在，则会将 cls 作为 key，cls(*args, **kw) 作为 value 存到 instances 中，否则，直接返回 instances[cls]。
```python
from functools import wraps
def singleton(cls):
	instance = {}
	@wraps(cls)
	def getinstance(*args,**kwargs):
		if cls not in instance:
			instance[cls] = cls(*args,**kwargs)
		return instance[cls]
	return getinstance

@singleton
class Myclass(object):
	pass

```