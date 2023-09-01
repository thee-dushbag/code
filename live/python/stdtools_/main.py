from aiohttp import web
from uvloop import install as install_uvloop
from faker import Faker
import aiohttp_mako as aim
import json
from mpack import print as rprint
from pathlib import Path

SRC_PATH = Path.cwd() / 'resrc'
STATIC_PATH = SRC_PATH / 'static'
MOVIE_PATH = Path(__file__).parent / 'movie'
TMP_PATH =  SRC_PATH / 'templates'
assert MOVIE_PATH.exists(), 'No movies to serve'

install_uvloop()

async def index(req: web.Request):
    print(f"Cookies Found: [{req.path}]: {req.cookies}")
    resp = web.Response(text="Hello There<br><a href=\"/line_page\">Line Page</a><br><a href=\"/movie_page\">Movie Page</a>", content_type='text/html')
    resp.set_cookie('name', 'Simon Nganga')
    return resp

@aim.template('home.mako')
async def page(req: web.Request):
    return {}

async def js(req: web.Request):
    text = await req.text()
    lines = json.loads(text)
    rprint("Lines Received:")
    rprint(lines['lines'])
    return web.json_response({'name': 'No Body'})

@aim.template('movie.mako')
async def movie(req: web.Request):
    movies = [path.name for path in MOVIE_PATH.iterdir()]
    return {'movies': movies}

app = web.Application()
aim.setup(app, str(TMP_PATH))

app.add_routes([
    web.get('/', index),
    web.get('/line_page', page), #type:ignore
    web.route('*', '/js', js),
    web.static('/static', str(STATIC_PATH)),
    web.static('/movie', str(MOVIE_PATH)),
    web.get('/movie_page', movie) #type:ignore
])
