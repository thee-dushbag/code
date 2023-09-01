from dataclasses import dataclass, field
from enum import auto, StrEnum
import json
from typing import Any, Awaitable, Callable, Iterable, TypeVar

from flask import request
K, V = TypeVar('K'), TypeVar('V')

@dataclass
class Request(dict[K, V]):
    url: 'URL'
    body: bytes = b''
    
    async def text(self) -> str:
        return self.body.decode()
    
    async def json(self):
        return json.loads(self.body)
    
    @property
    def method(self): return self.url.method

    @property
    def query(self): return self.url.query



class Response(dict[K, V]): ...

Handler = Callable[[Request], Awaitable[Any | Response]]

class METHOD(StrEnum):
    GET = auto()
    POST = auto()
    DELETE =auto()
    PUT = auto()

@dataclass
class URL:
    method: METHOD
    path: str
    query: dict[str, str] = field(default_factory=dict)
    query_qs: str = ''

    def __post_init__(self):
        self.query = {}
        self.normalize_query()

    def _get_query(self, query_qs: str) -> dict[str, str]:
        query: dict[str, str] = {}
        sections = query_qs.split('&')
        for section in sections:
            key, _, value = section.partition('=')
            if key: query[key] = value
        return query

    def _get_query_qs(self, query: dict[str, str]) -> str:
        query_qs = ''
        for key, value in query.items():
            query_qs += f'{key}={value}'
        return query_qs
    
    def normalize_query(self):
        q = self._get_query(self.query_qs)
        self.query.update(q)
        self.query_qs = self._get_query_qs(self.query)

    def get_url(self) -> str:
        return f'{self.method!s}:{self.path}'

    def __str__(self):
        self.normalize_query()
        return f'{self.path}?{self.query_qs}'

@dataclass
class URLDispatcher:
    handlers: dict[str, 'RouteDef'] = field(default_factory=dict)

    def addroutedef(self, routedef: 'RouteDef'):
        self.handlers[f'{routedef.method!s}:{routedef.prefix}'] = routedef

    def get_handler(self, url: URL):
        return self.handlers.get(url.get_url())

@dataclass
class RouteDef:
    method: METHOD
    prefix: str
    handler: Handler


@dataclass
class RouteTableDef:
    handlers: list[RouteDef] = field(default_factory=list)
    
    def __iter__(self):
        return iter(self.handlers)
    
    def route(self, method: METHOD, prefix: str):
        def _deco(handler: Handler) -> Handler:
            self.handlers.append(RouteDef(method, prefix, handler))
            return handler
        return _deco
    
    def get(self, prefix: str): return self.route(METHOD.GET, prefix)
    def post(self, prefix: str): return self.route(METHOD.POST, prefix)
    def delete(self, prefix: str): return self.route(METHOD.DELETE, prefix)
    def put(self, prefix: str): return self.route(METHOD.PUT, prefix)

@dataclass
class Application:
    router = URLDispatcher()

    def add_routes(self, routes: Iterable[RouteDef]):
        for routedef in routes:
            self.router.addroutedef(routedef)
    
    async def request(self, request: Request):
        if routedef := self.router.get_handler(request.url):
            return await routedef.handler(request)

@dataclass
class View:
    request: Request
    
    def _iter(self):
        handler = getattr(self, str(self.request.method).lower(), None)
        if handler is None: return None
        return handler()
    
    def __await__(self):
        handler = self._iter()
        if handler is None: yield
        else: yield from handler