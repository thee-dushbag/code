from dataclasses import dataclass
from typing import Callable, Optional, Type

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy.orm import Session as _Session
from sqlalchemy.orm import declarative_base, sessionmaker

APP_KEY = "database.person.app_key.mine.unique"
Base: Type = declarative_base()


class Person(Base):
    __tablename__ = "person"
    person_id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(40), index=True, unique=True)
    email = sa.Column(sa.String(50), nullable=False, unique=True)
    age = sa.Column(sa.Integer(), nullable=False)

    def todict(self):
        return dict(name=self.name, age=self.age, email=self.email, id=self.person_id)


@dataclass
class DatabaseModel:
    engine: sa.engine.Engine
    metadata: sa.MetaData
    Session: Callable[..., _Session]

    def create_session(self):
        return self.Session()


class PersonManager:
    def __init__(self, db: DatabaseModel) -> None:
        self.session = db.create_session()
        self.db = db

    def add_person(self, name: str, age: int | str, email: str) -> bool:
        try:
            self.session.add(Person(name=name, age=int(age), email=email))
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False

    def get_all_people(self):
        people = self.session.query(Person)
        yield from (p.todict() for p in people)

    def delete_person(self, pid: int) -> bool:
        try:
            person = self.session.query(Person).where(Person.person_id == pid).one()
            self.session.delete(person)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False


def manager_from_request(req: web.Request):
    db = req.app.get(APP_KEY, None)
    if db is None:
        raise KeyError(f"Run setup to setup the DatabaseModel")
    return PersonManager(db)


def init_database(dns: str):
    engine = sa.create_engine(dns)
    metadata: sa.MetaData = Base.metadata
    metadata.bind = engine
    metadata.create_all()
    Session = sessionmaker(engine)
    return DatabaseModel(
        engine=engine,
        metadata=metadata,
        Session=Session,
    )


def setup(app: web.Application, dns: str):
    db = init_database(dns)
    app[APP_KEY] = db
    return db
