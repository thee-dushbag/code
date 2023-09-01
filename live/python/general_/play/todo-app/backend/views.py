from aiohttp import web

ctype = 'text/html'
routes = web.RouteTableDef()

@routes.get('/hello')
async def index(req: web.Request):
    name = req.query.get('name', None) or 'stranger'
    html = f'<h1><center>Hello {name.title()}</center></h1>'
    resp = web.Response(text=html, content_type=ctype)
    return resp

@routes.get('/no')
async def not_found(req: web.Request):
    raise web.HTTPNotFound

@routes.get('/br')
async def bad_req(req: web.Request):
    raise web.HTTPBadRequest

def setup(app: web.Application) -> web.RouteTableDef:
    app.add_routes(routes)
    return routes