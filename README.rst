efweb
=====

这是一个简单的异步API服务器框架。

Install
-------

.. code:: shell

    pip install efweb

Basic EXample
-------------

.. code:: python

    import efweb.web
    import asyncio

    class Test(efweb.web.RequestHandler):
        async def get(self):
            return self.write_json({"success": True, 'params': self.get_arguments()})

        async def post(self):
            return self.write_json({"success": True, 'method': 'post', 'postdata': await self.get_post(), 'a': await self.get_argument('a')})

    class Test2(efweb.web.RequestHandler):
        async def get(self):
            match_info = await self.match_info
            return self.write_json({"success": True, 'Handler': 'test2', 'name': match_info['name']})

        async def post(self):
            # application/json
            return self.write_json({"success": True, 'method': 'post', 'postjson': await self.get_json()})

    routers = [(r'/', Test), (r'/user/{name}', Test2)]


    loop = asyncio.get_event_loop()
    loop.run_until_complete(efweb.web.init_app(loop, routers=routers))
    loop.run_forever()

Base Methods
------------

**初始化应用：**

::

    efweb.web.init_app(loop, routers=routers)

可选参数

``host`` : 服务器ip

``port`` ：端口号

``middlewares``: 拦截函数

``cors``: 是否跨域请求

**创建Handler：**

创建一个类，继承\ ``efweb.web.RequestHandler``,
重写\ ``get``\ 和\ ``post``\ 方法来处理请求。例子如下：

.. code:: python

    class Test(efweb.web.RequestHandler):
        async def get(self):
            return self.write_json({"success": True, 'method': 'get'})
        async def post(self):
            return self.write_json({"success": True, 'method': 'post'})

**路由配置：**

初始化应用的时候，传入router参数，内部是路由的tuple,第一个元素是url规则，第二个元素是handler，构建形式如下：

::

    routers = [
                (r'/', Test),
                (r'/user/{name}', Test2)
            ]

**获取url中携带的参数:**

.. code:: python

    self.get_arguments()  # 所有参数
    await self.get_argument('name', 'dufault') # 单一参数 (包括post表单中的参数)

**获取url中的参数：**

比如，/path/{name}

.. code:: python

    match_info = await self.match_info
    name = match_info[name]

**获取POST表单参数：**

.. code:: python

    await self.get_post()

**获取POST的JSON数据：**

.. code:: python

    await self.get_json()

**返回json数据：**

::

    self.write_json({})
    # or
    efweb.web.json_response()

**middleware:**

相当于一个拦截器，一个url被处理器处理前后增加一些操作，例如：

.. code:: python

    @efweb.web.middleware
    async def error_middleware(request, handler):
        if request.method == 'POST' and request.content_type != 'application/json':
            return efweb.web.json_response({'error': 'Request data must be a json type.'})
        response = await handler(request)
        print('after handller do something ...')
        return response

初始化应用的时候需要传入\ ``middlewares``\ 参数。

.. code:: python

    efweb.web.init_app(loop, routers=routers, middlewares=[error_middleware])