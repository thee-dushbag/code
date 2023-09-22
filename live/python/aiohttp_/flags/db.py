import enum as _enum
from dataclasses import dataclass
from typing import cast

import bcrypt as _bc
import model as _md
from aiohttp import web
from mpack import flags as _flg

APP_KEY = "application.db.model.testing.permissions"


class Perm(_enum.IntFlag):
    NONE = _enum.auto(0)
    SPEAK = _enum.auto()
    VIEW = _enum.auto()
    RUN = _enum.auto()
    READ = _enum.auto()
    WRITE = _enum.auto()

    @classmethod
    def interpret(cls, perm):
        return {
            name: _flg.flag_enabled(perm, value)
            for name, value in cls.__members__.items()
            if value != cls.NONE
        }

    @classmethod
    def get(cls, value: str):
        for name, _value in cls.__members__.items():
            if name.lower() == value.lower():
                return _value


@dataclass
class Database:
    session: _md._Session

    def update_user(self, user: _md.Users):
        self.session.add(user)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def add_user(self, user: _md.Users):
        user.password = hash_password(user.password)  # type:ignore
        self.update_user(user)

    def _get_user(self, cond) -> _md.Users | None:
        try:
            return self.session.query(_md.Users).where(cond).one()
        except Exception as e:
            self.session.rollback()

    def get_user_by_email(self, email: str) -> _md.Users:
        return self._get_user(_md.Users.email == email)

    def get_user_by_name(self, name: str) -> _md.Users:
        return self._get_user(_md.Users.name == name)

    def get_user_by_id(self, user_id: int) -> _md.Users:
        return self._get_user(_md.Users.user_id == user_id)

    def delete_user(self, user: _md.Users):
        try:
            self.session.delete(user)
        except Exception:
            ...

    def _perm(self, user: _md.Users, perm, switch):
        try:
            p = cast(int, user.permission)
            user.permission = switch(p, perm)  # type:ignore
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()

    def permitted(self, user: _md.Users, perm: int):
        p = cast(int, user.permission)
        return _flg.flag_enabled(p, perm)

    def grant(self, user: _md.Users, perm: int):
        self._perm(user, perm, _flg.flag_on)

    def deny(self, user: _md.Users, perm: int):
        self._perm(user, perm, _flg.flag_off)


def hash_password(password: str, _fmt="utf-8"):
    bpass = password.encode(_fmt)
    salt = _bc.gensalt()
    hpass = _bc.hashpw(bpass, salt)
    return hpass.decode(_fmt)


def check_password(password: str, hashed: str, _fmt="utf-8"):
    hpass = hashed.encode(_fmt)
    bpass = password.encode(_fmt)
    return _bc.checkpw(bpass, hpass)


def get_app_db(app: web.Application) -> Database:
    db = app.get(APP_KEY, None)
    if db is not None:
        return db
    raise KeyError("Database was not setup.")


def get_db(req: web.Request):
    return get_app_db(req.app)


def setup(app: web.Application, dns: str):
    db = _md.init_db(dns)
    udb = Database(db.session())
    app[APP_KEY] = udb
    return udb
