from aiohttp import web

async def stream(req: web.Request):
    return web.FileResponse("./resources/movie.mp4")

app = web.Application()
app.router.add_get('/stream', stream)

web.run_app(app)
