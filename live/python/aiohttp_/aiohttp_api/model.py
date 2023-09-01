from dataclasses import dataclass
from typing import Any, Type
from aiohttp import web
import sqlalchemy as sa
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    Session as _Session
)

APP_KEY = 'api.model.programming.aiohttp'
Base: Any = declarative_base()

# Actual Models Below
class User(Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)

# Database Pack
@dataclass
class Database:
    base: Type[Any]
    metadata: sa.MetaData
    maker: sessionmaker

    def new_session(self) -> _Session:
        return self.maker()


# Some Utility Functions
def get_app_database(app: web.Application) -> Database:
    db: Database | None = app.get(APP_KEY)
    assert isinstance(db, Database), \
        f'Expected a Database pack but found: {type(db)}'
    return db

def get_database(req: web.Request):
    return get_app_database(req.app)

def new_db_session(req: web.Request) -> _Session:
    db = get_database(req)
    return db.new_session()

# Setting up the database
def setup(app: web.Application, dns: str):
    metadata: sa.MetaData = Base.metadata
    engine = sa.create_engine(dns)
    metadata.create_all(engine)
    maker = sessionmaker(engine)
    db = Database(Base, metadata, maker)
    app[APP_KEY] = db
    return db