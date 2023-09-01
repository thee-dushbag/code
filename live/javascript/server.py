from aiohttp import web

def greeting(name: str) -> str:
    return f'Hello {name}, how was your day?'

async def greet(req: web.Request):
    name = req.query.get('name', 'stranger').title()
    return web.json_response({'result': greeting(name)})

routes = [
    web.get('/greet', greet, name='greet'),
    web.static('/', '.')
]

async def application() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app