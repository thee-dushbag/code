from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_security import SessionIdentityPolicy, setup as security_setup
from aiohttp import web
from model import Database

class UserAuthentication(AbstractAuthorizationPolicy):
    def __init__(self, db: Database) -> None:
        self.session = db.new_session()

    async def permits(self, identity, permission, context=None):
        return

    async def authorized_userid(self, identity):
        return

def setup(app: web.Application, db: Database):
    auth = UserAuthentication(db)
    identity = SessionIdentityPolicy()
    security_setup(app, identity, auth)