from typing import Callable, Mapping
from aiohttp import web
from aiohttp.web_request import Request
from yarl import URL
from utils import url_for
import model_helpers as mh
from aiohttp_security import (
    check_authorized,
    is_anonymous,
    remember,
)

url: Callable[..., URL]
routes = web.RouteTableDef()


@routes.view("/notes", name='note')
class NoteView(web.View):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.manager = mh.manager_from_request(request)

    async def _get_notes_public(self):
        q = self.request.query.get("user_id", None)
        if q is None:
            raise web.HTTPBadRequest
        try: user_id = int(q)
        except ValueError:
            raise web.HTTPBadRequest
        n = mh.get_all_user_public_notes(self.manager, user_id).all()
        notes = [note.todict() for note in n]
        resp = web.json_response(notes)
        await remember(self.request, resp, 'simon')
        return resp
    
    async def _get_all_notes(self, user_id: int):
        notes = mh.get_all_user_notes(self.manager, user_id).all()
        notes = [note.todict() for note in notes]
        return web.json_response(notes)

    async def get(self):
        if await is_anonymous(self.request):
            return await self._get_notes_public()
        user: mh.User = await check_authorized(self.request)
        return await self._get_all_notes(user.user_id)  # type:ignore

    async def _construct_note(self, src: Mapping, uid):
        title = src.get('title')
        text = src.get('text')
        access_id = src.get('access_id')
        return mh.Note(title=title, text=text, user_id=uid, access_id=access_id)

    async def post(self):
        user: mh.User = await check_authorized(self.request) #type:ignore
        data = await self.request.post()
        note: mh.Note = await self._construct_note(data, user.user_id)
        self.manager.add_note(note)
        raise web.HTTPFound(self.request.path)
    
    async def put(self):
        user: mh.User = await check_authorized(self.request) #type:ignore
        note_id = self.request.query.get('note_id', None)
        if note_id is None:
            raise web.HTTPBadRequest
        try: note_id = int(note_id)
        except ValueError: raise web.HTTPBadRequest
        note = self.manager.get_note_by_id(note_id)
        data = await self.request.post()
        title = data.get('title', None)
        text = data.get('text', None)
        if note is None:
            raise web.HTTPBadRequest
        if title: note.title = str(title) #type: ignore
        if text: note.text = str(text)#type: ignore
        self.manager.session.commit()

    async def delete(self):
        user: mh.User = await check_authorized(self.request) #type:ignore
        note_id = self.request.query.get('note_id', None)
        if note_id is None:
            raise web.HTTPBadRequest
        try: note_id = int(note_id)
        except ValueError: raise web.HTTPBadRequest
        note = self.manager.get_note_by_id(note_id)
        if note is None:
            raise web.HTTPBadRequest
        noted = note.todict()
        self.manager.delete_note(note_id)
        return web.json_response(noted)


@routes.view('/users', name='user')
class UserView(web.View):
    ...


def setup(app: web.Application, static_path: str):
    global url
    routes.static("/static", static_path, name="static")
    url = url_for(app)
    app.add_routes(routes)
    return routes


# @routes.get('/', name='root')
# async def index(req: web.Request):
#     raise web.HTTPFound(url('home'))

# @routes.get('/home', name='home')
# async def home(req: web.Request):
#     resp = web.Response(text='<h1>Home Page</h1><br><a href="/anon">Anonymous</a>')
#     resp.content_type = 'text/html'
#     return resp

# @routes.get('/anon', name='anon') #type: ignore
# @template('homepage.mako')
# async def anon(req: web.Request):
#     logged = not await is_anonymous(req)
#     return {'logged': '' if logged else 'not '}

# @routes.get('/login', name='login')
# async def log_jack_in(req: web.Request):
#     resp = web.HTTPFound(url('anon'))
#     await remember(req, resp, 'jack')
#     raise resp

# @routes.get('/logout', name='logout')
# async def log_jack_out(req: web.Request):
#     resp = web.HTTPFound(url('anon'))
#     await forget(req, resp)
#     raise resp

# @routes.get('/listen', name='listen')
# async def check_jack_listen(req: web.Request):
#     await check_permission(req, 'listen')
#     return web.Response(text="<h1>You Can Listen</h1>",
#                         content_type='text/html')

# @routes.get('/speak', name='speak')
# async def check_jack_speak(req: web.Request):
#     await check_permission(req, 'speak')
#     return web.Response(text="<h1>You Can Speak</h1>",
#                         content_type='text/html')
