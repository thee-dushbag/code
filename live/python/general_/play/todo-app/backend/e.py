from o import (
    Application,
    RouteTableDef,
    MiddlewareChain,
    Request,
    Response,
    ANotFound,
    AOKRedirect,
    APartialContent,
    ANotAuthorized,
)

routes = RouteTableDef()
middle = MiddlewareChain()


def catch_404(req, handler):
    try:
        return handler(req)
    except ANotFound as e:
        return Response(
            content="Modified 404 Response",
            status=404,
            reason=f"Path: {req['path']} was not found",
        )


def auth(req, handler):
    user, passwd = "username", "password"
    if user not in req:
        raise ANotAuthorized(f'{user} not found')
    if passwd not in req:
        raise ANotAuthorized(f'{passwd} not found')
    return handler(req)


middle.add_middleware(catch_404, auth)


@routes.add_route("hello")
def hello(req: Request):
    say_hi = lambda n: f"Hello {n}, how was your day?"
    name = "stranger"
    name = req.get("name", name).title()
    return Response(content=say_hi(name))


@routes.add_route("add")
def add(req: Request):
    x, y = req.get("x"), req.get("y")
    if not x or not y:
        raise APartialContent(f"Parameters x or y were not passed {x=} {y=}")
    return Response(content=x + y)


@routes.add_route("greet")
def greet(req: Request):
    req.path = "hello"
    resp = req.resolve()
    resp["warning"] = 'Please use endpoint "hello" next time'
    return resp


app = Application(routes, middle)

req = Request(
    path="hello", name="simon nganga", password="myPassword5052"
)
req.app = app
print(req.resolve())
req.path = "greet"
print(req.resolve())
