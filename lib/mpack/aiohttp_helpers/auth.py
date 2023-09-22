from typing import Any, Protocol

import basicauth
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION


class UserStore(Protocol):
    def auth_user(self, username: str, password: str) -> Any:
        ...


def try_bsdecode(basic_auth_str: str):
    try:
        username, password = basicauth.decode(basic_auth_str)
    except basicauth.DecodeError:
        return None, None
    else:
        return username, password


def create_check_basic_auth(db: UserStore):
    def check_basicauth(req: web.Request):
        if auth_ := req.headers.get(AUTHORIZATION):
            name, passwd = try_bsdecode(auth_)
            if name and passwd:
                if db.auth_user(name, passwd):
                    return name, passwd
            raise web.HTTPUnauthorized(reason="Authentication Failure")
        raise web.HTTPUnauthorized(reason="Use BasicAuth Please")

    return check_basicauth
