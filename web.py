"""
this is a sample async web frame.
"""
__version__ = '0.2'
__author__ = 'geb'

import asyncio, logging
from aiohttp import web
from aiohttp.web import middleware, json_response
from efweb import utils


class HTTPError(Exception):
    def __init__(self, status_code=500, log_message=None, *args, **kwargs):
        self.status_code = status_code
        self.log_message = log_message
        self.args = args
        self.reason = kwargs.get('reason', None)
        if log_message and not args:
            self.log_message = log_message.replace('%', '%%')

    def __str__(self):
        message = "HTTP %d: %s" % (
            self.status_code,
            self.reason or utils.responses.get(self.status_code, 'Unknown'))
        if self.log_message:
            return message + " (" + (self.log_message % self.args) + ")"
        else:
            return message


class MissingArgumentError(HTTPError):
    """Exception raised by `RequestHandler.get_argument`.

    This is a subclass of `HTTPError`, so if it is uncaught a 400 response
    code will be used instead of 500 (and a stack trace will not be logged).

    .. versionadded:: 3.1
    """
    def __init__(self, arg_name):
        super(MissingArgumentError, self).__init__(
            400, 'Missing argument %s' % arg_name)
        self.arg_name = arg_name


class RequestHandler(object):
    """use this class to encapsulate a handler.
    """

    def __init__(self, app):
        self._app = app

    async def __call__(self, request):
        self.request = request
        if request.method == 'POST':
            return await self.post()
        elif request.method == 'GET':
            return await self.get()
        elif request.method == 'PUT':
            return await self.put()
        elif request.method == 'DELETE':
            return await self.delete()

    async def get_argument(self, name, default=None):
        """get the argument in url or post body
        """
        data = dict(await self.request.post())
        if data:
            result = data.get(name, default)
        else:
            result = self.request.rel_url.query.get(name, default)
        if result is None:
            raise MissingArgumentError(name)
        return result

    async def get_arguments(self):
        """get all arguments in url
        """
        if self.request.rel_url.query:
            d = dict(self.request.rel_url.query)
        data = dict(await self.request.post())
        if data and d:
            d.update(data)
        return d

    async def get_post(self):
        """get all form post data
        """
        data = dict(await self.request.post())
        return data

    async def get_json(self):
        """get all post json type data
        """
        data = dict(await self.request.json())
        return data

    @property
    async def match_info(self):
        """get all match info"""
        return dict(self.request.match_info)

    async def get(self, *args, **kwargs):
        raise HTTPError(405)

    async def post(self, *args, **kwargs):
        raise HTTPError(405)

    async def put(self, *args, **kwargs):
        raise HTTPError(405)

    async def delete(self, *args, **kwargs):
        raise HTTPError(405)

    def write_json(self, res):
        """write json response
        """
        return web.json_response(res)


def add_route(app, routers):
    """add routers
    """
    for uri, handler in routers:
        if 'get' in handler.__dict__:
            app.router.add_route('GET', uri, handler(app))
        if 'post' in handler.__dict__:
            app.router.add_route('POST', uri, handler(app))
        if 'put' in handler.__dict__:
            app.router.add_route('PUT', uri, handler(app))
        if 'delete' in handler.__dict__:
            app.router.add_route('DELETE', uri, handler(app))



async def init_app(loop, routers, host='127.0.0.1', port=8000, middlewares=None):
    app = web.Application(loop=loop, middlewares=middlewares)
    add_route(app, routers)
    srv = await loop.create_server(app.make_handler(), host, port)
    print(f'Server started at http://{ host }:{ port }...')
    return srv



