import json
from aiohttp import web, hdrs
from utils import template
from config import get_config
from aiohttp_mako import setup as mako_setup
from mpack import print
from basicauth import decode

CONFIG_KEY = 'app.views.routes.maps'

@template('index.mako')
async def home(req: web.Request):
    return {}

async def sayhi(req: web.Request):
    return web.Response(text='Hello There? What\'s up.')

@web.middleware
async def basic_auth_middleware(req: web.Request, handler):
    if auth := req.headers.get(hdrs.AUTHORIZATION):
        if 'Basic' in auth:
            name, passwd = decode(auth)
            print(f"Basic auth used: {name!r} with {passwd!r}")
        else:
            print("Authentication used is not Basic Auth")
    else:
        print("Authorization not used.")
    return await handler(req)

async def sayhito(req: web.Request):
    data = await req.post()
    name = data.get('name', 'stranger')
    text = f'Hello {name}, how was your day?'
    return web.Response(text=text)

async def lines(req: web.Request):
    data = await req.post()
    lines = data.get('lines', '{}')
    lines = json.loads(str(lines)).get('data', [])
    print(f"Lines Received: {lines}")
    return web.Response(text='OK')

routes: list[web.RouteDef] = [
    web.get('/', home, name='index'),
    web.get('/sayhi', sayhi),
    web.post('/sayhito', sayhito),
    web.post('/lines', lines)
]

def setup(app: web.Application):
    app.add_routes(routes)
    config = get_config(app, CONFIG_KEY)
    app.router.add_static('/static', config.staticdir)
    mako_setup(app, config.templatedir)
    app.middlewares.append(basic_auth_middleware)
    return routes