# Python中的异步协程

# 什么是协程

协程，英文叫做 Coroutine，又称微线程，纤程，协程是一种用户态的轻量级线程。

协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈。

我们可以使用协程来实现异步操作，比如在网络爬虫场景下，我们发出一个请求之后，需要等待一定的时间才能得到响应，但其实在这个等待过程中，程序可以干许多其他的事情，等到响应得到之后才切换回来继续处理，这样可以充分利用 CPU 和其他资源，这就是异步协程的优势。

# 定义协程


    import asyncio
    
    async def execute(x):
        print('Number:', x)
    
    coroutine = execute(1)
    print('Coroutine:', coroutine)
    print('After calling execute')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine)
    print('After calling loop')

运行结果：

    Coroutine: <coroutine object execute at 0x036B58A0>
    After calling execute
    Number: 1
    After calling loop

- 先import Python里面大名鼎鼎的asyncio这个异步包，然后才可以使用 async 和 await。我们接着 async 定义了一个 execute() 方法，方法接收一个数字参数，方法执行之后会打印这个数字。
- 随后我们直接调用了这个方法，然而这个方法并没有执行，而是返回了一个 coroutine 协程对象。
- 随后我们使用 get_event_loop() 方法创建了一个事件循环 loop，并调用了 loop 对象的 run_until_complete() 方法将协程注册到事件循环 loop 中，然后启动。最后我们才看到了 execute() 方法打印了输出结果。
- 可见，async 定义的方法就会变成一个无法直接执行的 coroutine 对象，必须将其注册到事件循环中才可以执行
- 上文我们还提到了 task，它是对 coroutine 对象的进一步封装，它里面相比 coroutine 对象多了运行状态，比如 running、finished 等，我们可以用这些状态来获取协程对象的执行情况。


在上面的例子中，当我们将 coroutine 对象传递给 run_until_complete() 方法的时候，实际上它进行了一个操作就是将 coroutine 封装成了 task 对象，我们也可以显式地进行声明，如下所示：

    import asyncio
    
    async def execute(x):
        print('Number:', x)
        return x
    
    coroutine = execute(1)
    print('Coroutine:', coroutine)
    print('After calling execute')
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    print('Task:', task)
    loop.run_until_complete(task)
    print('Task:', task)
    print('After calling loop')

运行结果：

    Coroutine: <coroutine object execute at 0x034853C0>
    After calling execute
    Task: <Task pending coro=<execute() running at E:\test.py:3>>
    Number: 1
    Task: <Task finished coro=<execute() done, defined at E:\test.py:3> result=1>
    After calling loop

- 这里我们定义了 loop 对象之后，接着调用了它的 create_task() 方法将 coroutine 对象转化为了 task 对象
- 随后我们打印输出一下，发现它是 pending 状态。接着我们将 task 对象添加到事件循环中得到执行，
- 随后我们再打印输出一下 task 对象，发现它的状态就变成了 finished
- 同时还可以看到其 result 变成了 1，也就是我们定义的 execute() 方法的返回结果。

另外定义 task 对象还有一种方式，就是直接通过 asyncio 的 ensure_future() 方法，返回结果也是 task 对象，这样的话我们就可以不借助于 loop 来定义，即使我们还没有声明 loop 也可以提前定义好 task 对象，写法如下：

    import asyncio
    
    async def execute(x):
        print('Number:', x)
        return x
    
    coroutine = execute(1)
    print('Coroutine:', coroutine)
    print('After calling execute')
    task = asyncio.ensure_future(coroutine)
    print('Task:', task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print('Task:', task)
    print('After calling loop')

运行结果：

    Coroutine: <coroutine object execute at 0x02DF53C0>
    After calling execute
    Task: <Task pending coro=<execute() running at E:\test.py:3>>
    Number: 1
    Task: <Task finished coro=<execute() done, defined at E:\test.py:3> result=1>
    After calling loop

发现其效果都是一样的。

# 绑定回调


另外我们也可以为某个 task 绑定一个回调方法，来看下面的例子：

    import asyncio
    import requests
    
    async def request():
        url = 'https://www.baidu.com'
        status = requests.get(url)
        return status
    
    def callback(task):
        print('Status:', task.result())
    
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    task.add_done_callback(callback)
    print('Task:', task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print('Task:', task)

- 在这里我们定义了一个 request() 方法，请求了百度，返回状态码，但是这个方法里面我们没有任何 print() 语句。
- 随后我们定义了一个 callback() 方法，这个方法接收一个参数，是 task 对象，然后调用 print() 方法打印了 task 对象的结果。
- 这样我们就定义好了一个 coroutine 对象和一个回调方法，我们现在希望的效果是，当 coroutine 对象执行完毕之后，就去执行声明的 callback() 方法。

那么它们二者怎样关联起来呢？很简单，只需要调用 add_done_callback() 方法即可，我们将 callback() 方法传递给了封装好的 task 对象，这样当 task 执行完毕之后就可以调用 callback() 方法了。

同时 task 对象还会作为参数传递给 callback() 方法，调用 task 对象的 result() 方法就可以获取返回结果了。

运行结果：

    Task: <Task pending coro=<request() running at E:\test.py:4> cb=[callback() at E:\test.py:9]>
    Status: <Response [200]>
    Task: <Task finished coro=<request() done, defined at E:\test.py:4> result=<Response [200]>>

实际上不用回调方法，直接在 task 运行完毕之后也可以直接调用 result() 方法获取结果，如下所示：

    import asyncio
    import requests
    
    async def request():
        url = 'https://www.baidu.com'
        status = requests.get(url)
        return status
    
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    print('Task:', task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print('Task:', task)
    print('Task Result:', task.result())

运行结果是一样的：

    Task: <Task pending coro=<request() running at E:\test.py:4>>
    Task: <Task finished coro=<request() done, defined at E:\test.py:4> result=<Response [200]>>
    Task Result: <Response [200]>

# 多任务协程


上面的例子我们只执行了一次请求，如果我们想执行多次请求应该怎么办呢？我们可以定义一个 task 列表，然后使用 asyncio 的 wait() 方法即可执行，看下面的例子：

    import asyncio
    import requests
    
    async def request():
        url = 'https://www.baidu.com'
        status = requests.get(url)
        return status
    
    tasks = [asyncio.ensure_future(request()) for _ in range(5)]
    print('Tasks:', tasks)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        print('Task Result:', task.result())

这里我们使用一个 for 循环创建了五个 task，组成了一个列表，然后把这个列表首先传递给了 asyncio 的 wait() 方法，然后再将其注册到时间循环中，就可以发起五个任务了。最后我们再将任务的运行结果输出出来，运行结果如下：

    Tasks: [<Task pending coro=<request() running at E:\test.py:4>>,
    <Task pending coro=<request() running at E:\test.py:4>>,
    <Task pending coro=<request() running at E:\test.py:4>>, 
    <Task pending coro=<request() running at E:\test.py:4>>,
    <Task pending coro=<request() running at E:\test.py:4>>]
    Task Result: <Response [200]>
    Task Result: <Response [200]>
    Task Result: <Response [200]>
    Task Result: <Response [200]>
    Task Result: <Response [200]>

可以看到五个任务被顺次执行了，并得到了运行结果。

# 举例：爬虫，协程实现


前面说了这么一通，又是 async，又是 coroutine，又是 task，又是 callback，但似乎并没有看出协程的优势啊？反而写法上更加奇怪和麻烦了！

为了表现出协程的优势，最好的方法就是模拟一个需要等待一定时间才可以获取返回结果的网页，最好的方式是自己在本地模拟一个慢速服务器，这里我们选用 Flask,然后编写服务器代码如下：

    from flask import Flask
    import time
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        time.sleep(3)
        return 'Hello!'
    
    if __name__ == '__main__':
        app.run(threaded=True)

这里我们定义了一个 Flask 服务，主入口是 index() 方法，方法里面先调用了 sleep() 方法休眠 3 秒，然后接着再返回结果，也就是说，每次请求这个接口至少要耗时 3 秒，这样我们就模拟了一个慢速的服务接口。

注意这里服务启动的时候，run() 方法加了一个参数 threaded，这表明 Flask 启动了多线程模式，不然默认是只有一个线程的。

如果不开启多线程模式，同一时刻遇到多个请求的时候，只能顺次处理，这样即使我们使用协程异步请求了这个服务，也只能一个一个排队等待，瓶颈就会出现在服务端。所以，多线程模式是有必要打开的。

启动之后，**Flask 应该默认会在 127.0.0.1:5000 上运行**，运行之后控制台输出结果如下：

    * Serving Flask app "test" (lazy loading)
     * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

接下来我们再重新使用上面的方法请求一遍：

    import asyncio
    import requests
    import time
    
    start = time.time()
    async def request():
        url = 'http://127.0.0.1:5000'
        print('Waiting for', url)
        response = requests.get(url)
        print('Get response from', url, 'Result:', response.text)
    tasks = [asyncio.ensure_future(request()) for _ in range(5)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print('Cost time:', end - start)

在这里我们还是创建了五个 task，然后将 task 列表传给 wait() 方法并注册到时间循环中执行。

运行结果如下：

    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Cost time: 15.1424081325531

可以发现和正常的请求并没有什么两样，依然还是顺次执行的，耗时 15 秒，平均一个请求耗时 3 秒，说好的异步处理呢？

其实，要实现异步处理，我们得先要有挂起的操作，当一个任务需要等待 IO 结果的时候，可以挂起当前任务，转而去执行其他任务，这样我们才能充分利用好资源，**上面方法都是一本正经的串行走下来，连个挂起都没有，怎么可能实现异步？想太多了。**

要实现异步，接下来我们再了解一下 await 的用法，使用 await 可以将耗时等待的操作挂起，让出控制权。当协程执行的时候遇到 await，时间循环就会将本协程挂起，转而去执行别的协程，直到其他的协程挂起或执行完毕。

所以，我们可能会将代码中的 request() 方法改成如下的样子：

    async def request():
        url = 'http://127.0.0.1:5000'
        print('Waiting for', url)
        response = await requests.get(url)
        print('Get response from', url, 'Result:', response.text)

仅仅是在 requests 前面加了一个 await，然而执行以下代码，会得到如下报错：

    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Cost time: 15.094174861907959
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at E:\async.py:6> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "E:\async.py", line 9, in request
        response = await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at E:\async.py:6> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "E:\async.py", line 9, in request
        response = await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at E:\async.py:6> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "E:\async.py", line 9, in request
        response = await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at E:\async.py:6> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "E:\async.py", line 9, in request
        response = await requests.get(url)
    TypeError: object Response can't be used in 'await' expression
    Task exception was never retrieved
    future: <Task finished coro=<request() done, defined at E:\async.py:6> exception=TypeError("object Response can't be used in 'await' expression",)>
    Traceback (most recent call last):
      File "E:\async.py", line 9, in request
        response = await requests.get(url)
    TypeError: object Response can't be used in 'await' expression

这次它遇到 await 方法确实挂起了，也等待了，但是最后却报了这么个错，这个错误的意思是 requests 返回的 Response 对象不能和 await 一起使用，为什么呢？因为根据官方文档说明，await 后面的对象必须是如下格式之一：

- A native coroutine object returned from a native coroutine function，一个原生 coroutine 对象。
- A generator-based coroutine object returned from a function decorated with types.coroutine()，一个由 types.coroutine() 修饰的生成器，这个生成器可以返回 coroutine 对象。
- An object with an **await__ method returning an iterator，一个包含 __await** 方法的对象返回的一个迭代器。

reqeusts 返回的 Response 不符合上面任一条件，因此就会报上面的错误了。那么有的小伙伴就发现了，既然 await 后面可以跟一个 coroutine 对象，那么我用 async 把请求的方法改成 coroutine 对象不就可以了吗？所以就改写成如下的样子：

    import asyncio
    import requests
    import time
    
    start = time.time()
    async def get(url):
        return requests.get(url)
    
    async def request():
        url = 'http://127.0.0.1:5000'
        print('Waiting for', url)
        response = await get(url)
        print('Get response from', url, 'Result:', response.text)
    
    tasks = [asyncio.ensure_future(request()) for _ in range(5)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print('Cost time:', end - start)

这里我们将请求页面的方法独立出来，并用 async 修饰，这样就得到了一个 coroutine 对象，我们运行一下看看：

    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Cost time: 15.111292123794556

还是不行，它还不是异步执行，也就是说我们仅仅将涉及 IO 操作的代码封装到 async 修饰的方法里面是不可行的！我们必须要使用支持异步操作的请求方式才可以实现真正的异步，所以这里就需要 aiohttp 派上用场了。

# 使用aiohttp


aiohttp 是一个支持异步请求的库，利用它和 asyncio 配合我们可以非常方便地实现异步请求操作。我们将 aiohttp 用上来，将代码改成如下样子：

    import asyncio
    import aiohttp
    import time
    
    start = time.time()
    
    async def get(url):
        session = aiohttp.ClientSession()
        response = await session.get(url)
        result = await response.text()
        session.close()
        return result
    
    async def request():
        url = 'http://127.0.0.1:5000'
        print('Waiting for', url)
        result = await get(url)
        print('Get response from', url, 'Result:', result)
    
    tasks = [asyncio.ensure_future(request()) for _ in range(5)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print('Cost time:', end - start)

在这里我们将请求库由 requests 改成了 aiohttp，通过 aiohttp 的 ClientSession 类的 get() 方法进行请求，结果如下：

    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Waiting for http://127.0.0.1:5000
    Get response from http://127.0.0.1:5000 Result: Hello!
    Get response from http://127.0.0.1:5000 Result: Hello!
    Get response from http://127.0.0.1:5000 Result: Hello!
    Get response from http://127.0.0.1:5000 Result: Hello!
    Get response from http://127.0.0.1:5000 Result: Hello!
    Cost time: 3.0199508666992187

成功了！我们发现这次请求的耗时由 15 秒变成了 3 秒，耗时直接变成了原来的 1/5。
