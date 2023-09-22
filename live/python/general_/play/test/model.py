from datetime import datetime as dtime
from typing import Any, Callable, Type

import sqlalchemy as sa
from aiohttp import web
from attrs import define
from config import get_config
from sqlalchemy.orm import Session as _Session
from sqlalchemy.orm import (backref, declarative_base, relationship,
                            sessionmaker)

CONFIG_KEY = "database.models.key"

_Base: Type = declarative_base()


class User(_Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(20), index=True, unique=True)
    password = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, index=True)
    vperm_id = sa.Column(sa.Integer, sa.ForeignKey("permissions.vperm_id"))


class Note(_Base):
    __tablename__ = "notes"
    note_id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.user_id"))
    title = sa.Column(sa.String, index=True)
    body = sa.Column(sa.String(255), default=str())
    notes = relationship(User, backref=backref("notes"))
    created_on = sa.Column(sa.DateTime(), default=dtime.now)
    last_modified = sa.Column(sa.DateTime(), default=dtime.now, onupdate=dtime.now)


class VPerm(_Base):
    __tablename__ = "permissions"
    vperm_id = sa.Column(sa.Integer, primary_key=True)
    perm_name = sa.Column(sa.String, nullable=False)


@define
class _DatabasePack:
    engine: sa.engine.Engine
    metadata: sa.MetaData
    base: Type
    session_maker: Callable[..., _Session]


def setup(app: web.Application):
    config: Any = get_config(app, CONFIG_KEY)
    engine = sa.create_engine(config.dns)
    metadata: sa.MetaData = _Base.metadata
    metadata.create_all(engine)
    SessMaker = sessionmaker(engine)
    pack = _DatabasePack(engine, metadata, _Base, SessMaker)
    config.db_pack = pack
    return pack
