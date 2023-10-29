from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_security import check_permission
from .dataplugin import getdata, Perm, User

class UsersView(web.View):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.manager = getdata(request)

    async def post(self):
        data = await self.request.post()
        if not (username := data.get("username")):
            raise web.HTTPBadRequest(reason="Username not provided.")
        if not (password := data.get("password")):
            raise web.HTTPBadRequest(
                reason=f"Password not provided for account {username!r}"
            )
        self.manager.adduser(User(name=username, password=password, permission=Perm.READ_DATA))
        raise web.HTTPCreated(reason=f"Account created for user {username!r}")

    async def put(self):
        await check_permission(self.request, Perm.WRITE_USER)
        user = self.request.query.get("user", None)
        if user is None:
            raise web.HTTPBadRequest(reason="Username not provided")
        elif target_user := self.manager.getuser(user):
            data = await self.request.post()
            password = data.get("password", None)
            permission = data.get("permission", None)
            if permission is not None:
                if not permission.isnumeric():
                    raise web.HTTPBadRequest(
                        reason=f"Expected an integer value for permission, found: {permission!r}"
                    )
                target_user.permission = abs(int(permission))
            if password is not None:
                target_user.password = password
        return web.HTTPAccepted(reason="Operation was successful")

    async def delete(self):
        await check_permission(self.request, Perm.DELETE_USER)
        user = self.request.query.get("user", None)
        if userdata := self.manager.getuser(user):
            del self.manager.users[user]
            return web.json_response({"user": userdata.asdict()})

    async def get(self):
        await check_permission(self.request, Perm.READ_USER)
        user = self.request.query.get("user", None)
        if user is None:
            payload = {"users": self.manager.users.asdict()}
        elif target_user := self.manager.getuser(user):
            payload = {user: target_user.asdict()}
        return web.json_response(payload)


class DataView(web.View):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.manager = getdata(request)

    async def get(self):
        await check_permission(self.request, Perm.READ_DATA)
        return web.json_response({"data": self.manager.data})

    async def post(self):
        await check_permission(self.request, Perm.WRITE_DATA)
        data = await self.request.post()
        if ndata := data.get("data"):
            self.manager.setdata(ndata)
            return web.HTTPCreated(reason="New data was set.")
        raise web.HTTPBadRequest(reason="No data was sent.")

    async def delete(self):
        await check_permission(self.request, Perm.DELETE_DATA)
        data = self.manager.getdata()
        self.manager.setdata(None)
        return web.json_response({"result": data})


routes = [web.view("/data", DataView), web.view("/user", UsersView)]

def setup(app: web.Application):
    app.add_routes(routes)