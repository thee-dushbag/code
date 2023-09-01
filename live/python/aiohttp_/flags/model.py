from typing import Type
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Session as _Session, sessionmaker
from dataclasses import dataclass

Base: Type = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    name = sa.Column(sa.String, index=True, nullable=False, unique=True)
    email = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)
    permission = sa.Column(sa.Integer)


@dataclass
class Database:
    base: Type
    engine: sa.engine.Engine
    maker: sessionmaker
    metadata: sa.MetaData

    def session(self) -> _Session:
        return self.maker()


def init_db(dns: str) -> Database:
    engine = sa.create_engine(dns)
    metadata: sa.MetaData = Base.metadata
    metadata.create_all(engine)
    maker = sessionmaker(engine)
    return Database(Base, engine, maker, metadata)
