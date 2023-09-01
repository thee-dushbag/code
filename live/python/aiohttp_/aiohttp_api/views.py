from typing import cast
from aiohttp import web
import utils, model

async def add_user(req: web.Request):
    data = await req.post()
    username = cast(str | None, data.get('username', None))
    password = cast(str | None, data.get('password', None))
    if not (username and password):
        raise web.HTTPBadRequest
    session = model.new_db_session(req)
    if utils.add_user(session, username, password):
        raise web.HTTPCreated
    raise web.HTTPConflict(reason='Please use other name/password')


routes = [
    web.post('/user', add_user)
]

def setup(app: web.Application):
    app.add_routes(routes)