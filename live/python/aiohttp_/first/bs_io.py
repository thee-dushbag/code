from aiohttp import web

routes = web.RouteTableDef()
email_rpat = r"(?P<username>[0-9a-z._-]+)@(?P<provider>[a-z]+)(?P<domain>\.[a-z]+)"


@routes.get("/")
async def hello(req: web.Request):
    print(f"Request Received:[{req.path}]: {req.remote} :[{req.method}]")
    return web.Response(text="Getting Data")


@routes.post("/post")
async def post(req: web.Request):
    print(f"Request Received:[{req.path}]: {req.remote} :[{req.method}]")
    return web.Response(text="Posting Data")


@routes.put("/put")
async def put(req: web.Request):
    print(f"Request Received:[{req.path}]: {req.remote} :[{req.method}]")
    return web.Response(text="Putting Data")


@routes.get("/emails/{email:email_rpat}/section".replace("email_rpat", email_rpat))
async def email_section(req: web.Request):
    email = req.match_info.get("email", "someemail@gmail.com")
    text = f"Your email is {email}. You are in Section."
    return web.Response(text=text)


@routes.get("/users/{username}/section")
async def username_section(req: web.Request):
    name = req.match_info.get("username", "Stranger").title()
    text = f"Hello {name}, how was your day? You are in Section."
    return web.Response(text=text)


@routes.route("*", "/all")
async def all_(req: web.Request):
    print(f"Request Received:[{req.path}]: {req.remote} :[{req.method}]")
    return web.Response(text="All methods allowed")


@routes.get("/get_data", name="data")
async def get_data(req: web.Request):
    data = dict(req.query)
    url = req.app.router["data"].url_for().with_query(data).__str__()
    data["url_"] = url
    return web.json_response(data)


class ClassHandler:
    async def say_hi(self, req: web.Request):
        name = req.match_info.get("name", "stranger").title()
        text = f"Hello {name}, how was your day?"
        return web.Response(text=text)


handler = ClassHandler()


@routes.view("/interact")
class Interact(web.View):
    async def get(self):
        return web.Response(text="Interact.get method")

    async def post(self):
        return web.Response(text="Interact.post method")

    async def put(self):
        return web.Response(text="Interact.put method")

    async def patch(self):
        return web.Response(text="Interact.patch method")


app = web.Application()
# app.add_routes([web.get('/', hello)])
app.add_routes(routes)
app.add_routes(
    [web.get("/handler/{name}", handler.say_hi)]  # , web.view("/interact", Interact)]
)
