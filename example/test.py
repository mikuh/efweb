import efweb.web
import asyncio


@efweb.web.middleware
async def error_middleware(request, handler):
    if request.method == 'POST' and request.content_type != 'application/json':
        return efweb.web.json_response({'error': 'Request data must be a json type.'})
    response = await handler(request)
    return response



class Test(efweb.web.RequestHandler):
    async def get(self):
        print(self.request.content_type)  # application/octet-stream
        return self.write_json({"success": True, 'params': self.get_arguments()})

    async def post(self):
        print(self.request.content_type)  # application/x-www-form-urlencoded
        return self.write_json({"success": True, 'method': 'post', 'postdata': await self.get_post()})

class Test2(efweb.web.RequestHandler):
    async def get(self):
        match_info = await self.match_info
        return self.write_json({"success": True, 'Handler': 'test2', 'name': match_info['name']})

    async def post(self):
        # application/json
        return self.write_json({"success": True, 'method': 'post', 'postjson': await self.get_json()})

routers = [(r'/', Test), (r'/user/{name}', Test2)]


loop = asyncio.get_event_loop()
loop.run_until_complete(efweb.web.init_app(loop, routers=routers, middlewares=[error_middleware]))
loop.run_forever()
