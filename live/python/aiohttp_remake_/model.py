from dataclasses import dataclass
from typing import Callable, Type

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as _Session
from sqlalchemy.orm import declarative_base, sessionmaker

APP_KEY = "aiohttp.security.test.session.database.model"


@dataclass
class DatabaseModel:
    engine: sa.engine.Engine
    metadata: sa.MetaData
    Session: Callable[..., _Session]

    def create_session(self):
        return self.Session()


Base: Type = declarative_base()


class Access(Base):
    __tablename__ = "access"
    access_id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(20), nullable=False, unique=True)
    description = sa.Column(sa.String(200), default=str())


class User(Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(40), index=True, unique=True, nullable=False)
    email = sa.Column(sa.String(60), index=True, unique=True, nullable=False)
    password = sa.Column(sa.String(50), nullable=False)

    def todict(self):
        return dict(name=self.name, email=self.email, user_id=self.user_id)


class Note(Base):
    __tablename__ = "notes"
    note_id = sa.Column(sa.Integer(), primary_key=True)
    access_id = sa.Column(sa.Integer(), sa.ForeignKey("access.access_id"))
    user_id = sa.Column(sa.Integer(), sa.ForeignKey("users.user_id"))
    text = sa.Column(sa.String(255), default=str())
    title = sa.Column(sa.String(50), nullable=False, index=True)

    def todict(self):
        return dict(
            title=self.title,
            text=self.text,
            user_id=self.user_id,
            note_id=self.note_id,
            access_id=self.access_id,
        )


def init_database(dns: str):
    engine = sa.create_engine(dns)
    metadata: sa.MetaData = Base.metadata
    metadata.create_all(engine)
    Session = sessionmaker(engine)
    return DatabaseModel(engine, metadata, Session)


def insert_access_rights(md: DatabaseModel):
    private = Access(
        access_id=1, name="PRIVATE", description="Only The Owner Can Access This Note"
    )
    public = Access(
        access_id=2, name="PUBLIC", description="EveryOne Can Access This Note"
    )
    session = md.create_session()
    session.add_all((private, public))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def setup(app: web.Application, dns: str):
    db = init_database(dns)
    insert_access_rights(db)
    app[APP_KEY] = db
    return db
