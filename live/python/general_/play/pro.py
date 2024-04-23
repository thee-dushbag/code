from os import getenv
from pathlib import Path

from aiohttp import web
from aiohttp_mako import setup, template

HOST, PORT = getenv("STATICS_HOST", "localhost"), 5052
path = Path(__file__).parent

@template("page.mako")
async def page(req: web.Request):
    pgcount = req.query.get("pages", "5")
    pgcount = abs(int(pgcount))
    pgcount = max(1, min(50, pgcount))
    return {"pages": pgcount, "STATICS_HOST": HOST}


app = web.Application()
app.router.add_get("/", page)  # type:ignore
setup(app, str(path))

web.run_app(app, host=HOST, port=PORT)
