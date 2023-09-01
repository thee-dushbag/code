from dataclasses import dataclass
import sqlalchemy as sa, typing as ty
from .models import Base
from sqlalchemy import orm

@dataclass
class DB:
    base: ty.Type
    maker: orm.sessionmaker[orm.Session]
    engine: sa.engine.Engine
    metadata: sa.MetaData

def init_db(dns: str) -> DB:
    engine = sa.create_engine(dns)
    metadata: sa.MetaData = Base.metadata # type: ignore
    metadata.create_all(engine)
    maker = orm.sessionmaker(engine)
    return DB(Base, maker, engine, metadata)
