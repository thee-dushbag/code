from aiohttp_security.abc import AbstractAuthorizationPolicy


class UserLoginAuthorization(AbstractAuthorizationPolicy):
    async def permits(self, identity, permission, context=None):
        ...

    async def authorized_userid(self, identity):
        ...
