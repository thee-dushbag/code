from typing import Any, Callable, Coroutine, cast
from aiohttp import web
from jinja2.utils import Namespace
from jinja2 import Environment, FileSystemLoader
import aiohttp_jinja2 as aji

APP_KEY = "My Fucking AppKey"

loader = FileSystemLoader("./templates")


def page_template(page_name: str, app_key: str | None = None):
    app_key = app_key or APP_KEY

    def page_renderer(page: str):
        def wrapper(handler: Callable[..., Coroutine]):
            async def receive_request(request: web.Request, *args, **kwargs):
                data = await handler(request, *args, **kwargs)
                env: Environment = request.app[app_key]
                main_page = env.get_template(page_name)
                text: str = main_page.render(
                    page=page, data=Namespace(**data, request=request)
                )
                return web.Response(text=text, content_type='text/html')

            return receive_request

        return wrapper

    return page_renderer


pages = page_template("page.html")
routes = web.RouteTableDef()


@routes.get("/")
@pages("upload")
async def index(req: web.Request):
    return {"name": "Simon Nganga"}


@routes.post('/login', name='login')
async def login(req: web.Request):
    data = await req.post()
    username = data['username']
    password = data['password']
    print(f"Login Attempt: {username=} {password=}")
    return web.HTTPSeeOther('/')


@routes.post('/upload_', name='file_uploa')
async def upload_file(req: web.Request):
    data = await req.post()
    file = cast(web.FileField, data['file'])
    username = cast(str, data['username'])
    print(f"File Uploaded: {username=} {file=} {type(file)=}")
    return web.HTTPSeeOther('/')

@routes.post('/upload', name='file_upload')
async def upload_file_multipart(req: web.Request):
    fields = await req.multipart()
    username, file = '', ''
    async for field in fields:
        if field.name == 'username':
            username = await field.text()
        if field.name == 'file':
            file = field.filename
    print(f"File Uploaded: {username=} {file=} {type(file)=}")
    return web.HTTPSeeOther('/')

app = web.Application()
env = aji.setup(app, loader=loader, app_key=APP_KEY)
app.add_routes(routes)
