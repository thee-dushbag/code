from aiohttp import web
from mpack.aiohttp_helpers.mako_ import page_template
from db_utils import add_user, get_user, del_user
from mpack.aiohttp_helpers.mako_ import get_url

routes = web.RouteTableDef()
pages = page_template('page.mako')

@routes.get('/', name='index')
@pages('home')
async def index(req: web.Request):
    return {}

@routes.get('/say_hi', name='say_hi')
@pages('say_hi')
async def say_hi(req: web.Request):
    name = req.query.get('name', 'stranger')
    return {'name': name}

@routes.post('/signup_post', name='signup_post')
async def signup_post(req: web.Request):
    url = get_url(req)
    data = await req.post()
    name = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if uid := await add_user(req, name, password, email):
        raise web.HTTPSeeOther(url('user', user_id=uid))
    raise web.HTTPSeeOther(url('index'))

async def show_user_str(user):
    return (
        f'NAME: {user.name}\n'
        f'EMAIL: {user.email}\n'
        f'PASSWORD: {user.password}'
    )

@routes.get('/user/{user_id:\d+}', name='user')
async def user_page(req: web.Request):
    user_id = req.match_info.get('user_id')
    user = await get_user(req, user_id)
    if not user:
        url = get_url(req)
        raise web.HTTPSeeOther(url('index'))
    ustr = await show_user_str(user)
    return web.Response(text=ustr)


@routes.get('/del_user/{user_id:\d+}', name='del_user')
async def del_user_(req: web.Request):
    user_id = req.match_info.get('user_id')
    if await del_user(req, user_id):
        return web.Response(text=f"User {user_id} deleted")
    return web.Response(text=f"User {user_id} NOT deleted")