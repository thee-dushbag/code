import enum
import json
from pathlib import Path

import attrs
from aiohttp import web

APP_KEY = "database_user_resources"
DEFAULT_ID = -1
GROUP_NAME = "Resource User Group"


@enum.unique
class Permission(enum.IntEnum):
    PRIVATE = enum.auto()
    PROTECTED = enum.auto()
    PUBLIC = enum.auto()


@enum.unique
class IdType(enum.IntEnum):
    GROUPID = enum.auto()
    USERID = enum.auto()
    RESRCID = enum.auto()


@attrs.define(slots=True, kw_only=True)
class User:
    uid: int = attrs.field(default=DEFAULT_ID)
    name: str
    password: str
    email: str
    groups: list[int] = attrs.field(factory=list)


def _permission_int_converter(perm: int | Permission) -> Permission:
    return Permission(perm)


@attrs.define(slots=True, kw_only=True)
class Resourse:
    rid: int = attrs.field(default=DEFAULT_ID)
    permission: Permission = attrs.field(
        default=Permission.PROTECTED, converter=_permission_int_converter
    )
    owner: int
    resource: str


@attrs.define(slots=True, kw_only=True)
class Group:
    gid: int = attrs.field(default=DEFAULT_ID)
    groupname: str = attrs.field(default=GROUP_NAME)
    members: list[int] = attrs.field(factory=list)
    groupdesc: str = attrs.field(default="This is a resource Group")


@attrs.define(slots=True)
class Database:
    users: list[User] = attrs.field(factory=list)
    resources: list[Resourse] = attrs.field(factory=list)
    groups: list[Group] = attrs.field(factory=list)

    def to_json(self) -> dict:
        users = [attrs.asdict(user) for user in self.users]
        resources = [attrs.asdict(resrc) for resrc in self.resources]
        groups = [attrs.asdict(group) for group in self.groups]
        return dict(users=users, resources=resources, groups=groups)

    @classmethod
    def from_json(cls, data: dict):
        users = [User(**u) for u in data.get("users", [])]
        resources = [Resourse(**r) for r in data.get("resources", [])]
        groups = [Group(**r) for r in data.get("groups", [])]
        return Database(users, resources, groups)

    def merge_db(self, db: "Database"):
        self.users = [*self.users, *db.users]
        self.resources = [*self.resources, *db.resources]
        self.groups = [*self.groups, *db.groups]


def _file_db_helper(file: Path | str) -> Path:
    f = Path(str(file))
    if not f.exists():
        f.touch()
    assert f.is_file(), f"database file is not a file: {f!r}"
    return f


def save_database(db: Database, file: str | Path):
    f = _file_db_helper(file)
    data = db.to_json()
    if f.exists():
        f.unlink()
    f.write_text(json.dumps(data))


def load_database(file: str | Path):
    f = _file_db_helper(file)
    content = f.read_text() or "{}"
    data = json.loads(content)
    return Database.from_json(data)


def get_app_db(app) -> Database:
    db = app.setdefault(APP_KEY, Database())
    assert (
        type(db) == Database
    ), f"Database type error, expected db of type Database, got {type(db)}"
    return db


def get_db(req) -> Database:
    return get_app_db(req.app)


def database_ctx_handler(file: str | Path):
    async def save_load_db_ctx(app: web.Application):
        db = load_database(file)
        _db = get_app_db(app)
        db.merge_db(_db)
        app[APP_KEY] = db
        yield
        save_database(db, file)

    return save_load_db_ctx


def setup(app: web.Application, file: str | Path):
    db_ctx = database_ctx_handler(file)
    app.cleanup_ctx.append(db_ctx)
