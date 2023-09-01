from typing import cast
from aiohttp import web
import aiohttp_jinja2 as aji
from jinja2.loaders import FileSystemLoader
from models import verify_login, add_user, get_user_files, add_file

logged_in: list[str] = []
routes = web.RouteTableDef()
app = web.Application()
aji.setup(app, loader=FileSystemLoader('./templates'))

@routes.get('/', name='homepage')
@aji.template('home.html')
async def index(req: web.Request):
    return {}

@routes.get('/logout/{username}', name='logout')
async def logout_get(req: web.Request):
    loc = req.app.router['homepage'].url_for()
    username = req.match_info.get('username', '')
    if username in logged_in:
        logged_in.pop(logged_in.index(username))
    raise web.HTTPFound(loc)

@routes.get('/loginpage', name='loginpage')
@aji.template('loginpage.html')
async def login_get(req: web.Request):
    return {}

@routes.get('/signuppage', name='signuppage')
@aji.template('signuppage.html')
async def signup_get(req: web.Request):
    return {}

@routes.get('/userpage/{username}', name='userpage')
@aji.template('userpage.html')
async def user_page(req: web.Request):
    username = req.match_info.get('username', None)
    if not username or username not in logged_in:
        loc = req.app.router['loginpage'].url_for()
        raise web.HTTPFound(loc)
    files = await get_user_files(username)
    return {'username': username, 'files': files}

@routes.post('/submitfile/{username}')
async def submit_file(req: web.Request):
    username = req.match_info.get('username', None)
    if not username or username not in logged_in:
        loc = req.app.router['loginpage'].url_for()
        raise web.HTTPSeeOther(loc)
    data = await req.post()
    print(f'\x1b[91;1mPosted data: \x1b[0m{dict(data)} {data}')
    # file = cast(web.FileField, data['userfile'])
    # filename = file.filename
    # with open(f'./user_files/{filename}', 'wb') as f:
    #     content = file.file.read()
    #     size = len(content)
    #     f.write(content)
    # await add_file(username, filename, size)
    loc = req.app.router['userpage'].url_for(username=username)
    raise web.HTTPSeeOther(loc)

@routes.post('/loginpost', name='loginpost')
async def login_post(req: web.Request):
    data = await req.post()
    username: str = str(data['username'])
    password: str = str(data['password'])
    print("Loginpost")
    if await verify_login(username, password):
        logged_in.append(username)
        location = req.app.router['userpage'].url_for(username=username)
        raise web.HTTPSeeOther(location)
    location = req.app.router['loginpage'].url_for()
    raise web.HTTPSeeOther(location)

@routes.post('/signuppost', name='signuppost')
async def signup_post(req: web.Request):
    data = await req.post()
    username: str = str(data['username'])
    email: str = str(data['email'])
    password: str = str(data['password'])
    if await add_user(username, email, password):
        location = req.app.router['loginpage'].url_for()
        raise web.HTTPSeeOther(location)
    location = req.app.router['signuppage'].url_for()
    raise web.HTTPSeeOther(location)

app.add_routes(routes)