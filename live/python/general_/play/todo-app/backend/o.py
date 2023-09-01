from functools import partial, reduce
from attrs import define, field

from typing import Callable, Union, cast


class AError(Exception):
    status = 100

    @classmethod
    def reason(cls):
        return getattr(cls, "message", cls.__name__)


class AClientError(AError):
    status = 400
    message = "Error Occured at Client Level"


class ANotAuthorized(AClientError):
    status = 409
    message = "Please provide username and password"

class APartialContent(AClientError):
    status = 403
    message = "Pass All Parameters Please"


class ANotFound(AClientError):
    status = 404
    message = "Request path Not Found"


class AServerError(AError):
    status = 500
    message = "Sever got itself in trouble"


class AOKStatus(AError):
    status = 200


class AOKRedirect(AError):
    status = 300

    def __init__(self, location) -> None:
        self.location = location

    def locate(self, req):
        req.path = self.location
        return req.resolve()


class Response(dict):
    def __init__(self, **kwd):
        super().__init__(**kwd)
        self.status
        self.content

    @property
    def status(self):
        return self.setdefault("status", 200)

    @property
    def content(self):
        return self.get('content', '')
    
    @status.setter
    def status(self, value):
        self['status'] = value

    @content.setter
    def content(self, value):
        self['content'] = value

class Request(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app: Union['Application', None] = None
        self.path

    def resolve(self):
        if isinstance(self.app, Application):
            return self.app.make_request(self)
        raise Exception("Application Not attached to the request")

    @property
    def path(self) -> str:
        return self.get("path", None)
    
    @path.setter
    def path(self, value):
        self['path'] = value


_Handler = Callable[[Request], Response]
_Middleware = Callable[[Request, _Handler], Response]


class MiddlewareChain(list[_Middleware]):
    def add_middleware(self, *mids: _Middleware):
        for mid in mids:
            self.append(mid)

    def _chain(self, handler) -> _Handler:
        cover = lambda r: handler(r)
        for mid in self:
            cover = partial(mid, handler=cover)  # type:ignore
        return cast(_Handler, cover)

    def handle(self, handler: _Handler) -> _Handler:
        return self._chain(handler)

class RouteTableDef(dict[str, _Handler]):
    def add_route(self, key: str):
        def add_handler(func: _Handler):
            self[key] = func

        return add_handler


def make_resp_from_error(error: AError):
    resp = Response(status=error.status, reason=error.reason(), text=str(error))
    return resp


def _catch_system_error(req: Request, handler):
    try:
        return handler(req)
    except AError as e:
        raise e
    except Exception as e:
        raise AServerError(str(e))


def _redirect_middleware(req, handler):
    try:
        return handler(req)
    except AOKRedirect as e:
        return e.locate(req)


def _base_middle_ware(req: Request, handler):
    try:
        return handler(req)
    except AError as e:
        return make_resp_from_error(e)


def _setup_middlewares(handler):
    mid = partial(_redirect_middleware, handler=handler)
    mid = partial(_catch_system_error, handler=mid)
    mid = partial(_base_middle_ware, handler=mid)
    return mid


@define
class Application:
    routes: RouteTableDef = field(factory=RouteTableDef)
    middlewares: MiddlewareChain = field(factory=MiddlewareChain)
    handler: _Handler = field(init=False)

    def __attrs_post_init__(self):
        handler = self._resolve_handler
        handler = self.middlewares.handle(handler)
        mid = _setup_middlewares(handler)
        self.handler = mid

    def _resolve_handler(self, req: Request):
        req.app = self  # type:ignore
        handler = self.routes.get(req.path, None)
        if handler is None:
            raise ANotFound(f"Path: {req.path!r} not found")
        return handler(req)

    def make_request(self, req: Request) -> Response:
        return self.handler(req)
