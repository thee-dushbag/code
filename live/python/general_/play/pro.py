from aiohttp import web
from aiohttp_mako import setup, template
from pathlib import Path
from os import getenv
HOST, PORT = getenv('STATICS_HOST', 'localhost'), 5052

@template('page.mako')
async def page(req: web.Request):
    pgcount = req.query.get('pages', '5')
    try:
        pgcount = abs(int(pgcount))
        if pgcount > 50:
            pgcount = 50
        if pgcount < 1:
            raise Exception
    except Exception:
        raise web.HTTPBadRequest(reason=f'Pages must be a positive integer >=1: {pgcount!r}')
    return {'pages': pgcount, 'STATICS_HOST': HOST}

app = web.Application()
app.router.add_get('/', page) #type:ignore
setup(app, '/home/simon/Content/code/live/python/general_/play')

web.run_app(app, host=HOST, port=PORT)