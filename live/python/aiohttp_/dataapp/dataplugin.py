from pathlib import Path
import typing as ty, enum as _e
from aiohttp import web

APP_KEY = "data.plugin.aiohttp.userdata"
USERS_KEY = "users"
DATA_KEY = "data"


class UserCollection(dict[str, "User"]):
    def asdict(self) -> dict[str, dict[str, str | int]]:
        return {name: user.asdict() for name, user in self.items()}


DataType: ty.TypeAlias = str | None


class Perm(_e.IntFlag):
    NONE: int = _e.auto(0)
    READ_DATA: int = _e.auto()
    WRITE_DATA: int = _e.auto()
    DELETE_DATA: int = _e.auto()
    READ_USER: int = _e.auto()
    WRITE_USER: int = _e.auto()
    DELETE_USER: int = _e.auto()


class User:
    def __init__(
        self, *, name: str, password: str, permission: int = Perm.NONE
    ) -> None:
        self._name = name
        self.password: str = password
        self.permission: int = permission

    @property
    def name(self) -> str:
        return self._name

    def asdict(self) -> dict[str, str | int]:
        return dict(name=self._name, password=self.password, permission=self.permission)


class Persister(ty.Protocol):
    def load(self) -> "Manager": ...

    def save(self, manager: "Manager") -> None: ...


class AbstractFilePersisterMixin:
    def __init__(self, path: Path) -> None:
        self.path: Path = path

    def _load(self, loader) -> "Manager":
        with self.path.open() as f:
            dictdata = loader(f)
        userslist = [User(**user) for user in dictdata.get(USERS_KEY, [])]
        users = {user.name: user for user in userslist}
        data = dictdata.get(DATA_KEY, None)
        return Manager(users=UserCollection(users), data=data)

    def _save(self, dumper, manager: "Manager"):
        with self.path.open("w") as f:
            dumper(
                {
                    USERS_KEY: list(manager.users.asdict().values()),
                    DATA_KEY: manager.data,
                },
                f,
            )


class JsonPersister(AbstractFilePersisterMixin):
    def load(self) -> "Manager":
        import json

        return self._load(json.load)

    def save(self, manager: "Manager") -> None:
        import json

        self._save(json.dump, manager)


class YamlPersister(AbstractFilePersisterMixin):
    def load(self) -> "Manager":
        import yaml

        return self._load(yaml.safe_load)

    def save(self, manager: "Manager") -> None:
        import yaml

        self._save(yaml.safe_dump, manager)


class Manager:
    def __init__(
        self, users: UserCollection | None = None, data: DataType = None
    ) -> None:
        self.users: UserCollection = UserCollection(users or {})
        self.data: DataType = data or None

    def adduser(self, user: User):
        if user.name in self.users:
            raise web.HTTPBadRequest(reason="Username already taken.")
        self.users[user.name] = user

    def getuser(self, username: str) -> User:
        if user := self.users.get(username):
            return user
        raise web.HTTPNotFound(reason=f"User {username} was not found.")

    def setdata(self, data: DataType):
        self.data = data

    def getdata(self) -> DataType:
        return self.data

    def validate(self, user: User):
        auser = self.getuser(user.name)
        return auser.password == user.password


def _persister(persister: Persister):
    async def bjob(app: web.Application):
        manager = persister.load()
        app[APP_KEY] = manager
        yield
        persister.save(manager)

    return bjob


def getappdata(app: web.Application) -> Manager:
    if manager := app.get(APP_KEY):
        return manager
    raise Exception(
        "Data plugin was not set. Call setup(app, persister) to initialize."
    )


def getdata(req: web.Request) -> Manager:
    return getappdata(req.app)


def setup(app: web.Application, persister: Persister):
    app.cleanup_ctx.append(_persister(persister))
