from typing import cast

import db as _db
from aiohttp import web
from aiohttp_security import setup as security_setup
from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_security.session_identity import SessionIdentityPolicy
from aiohttp_session import setup as session_setup
from aiohttp_session.redis_storage import RedisStorage
from mpack import flags
from redis.asyncio import Redis


async def create_key(user: _db._md.Users):
    return f"Identity.{user.name}.{user.email}"


async def get_user(key: str):
    _, _, details = key.partition(".")
    name, _, email = details.partition(".")
    return name, email


class UsersAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, db: _db.Database) -> None:
        self.db = db

    async def permits(self, identity: str, permission: int, context=None):
        if user := await self.authorized_userid(identity):
            p = cast(int, user.permission)
            return flags.flag_enabled(p, permission)

    async def authorized_userid(self, identity: str):
        n, e = await get_user(identity)
        return self.db.get_user_by_name(n)


def setup(app: web.Application, db: _db.Database, max_age=30):
    storage = RedisStorage(Redis(), max_age=max_age)
    auth_policy = UsersAuthorizationPolicy(db)
    identity_policy = SessionIdentityPolicy()
    security_setup(app, identity_policy, auth_policy)
    session_setup(app, storage)
