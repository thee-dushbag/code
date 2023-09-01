import sqlalchemy as sa
from typing import Type
from sqlalchemy.orm import declarative_base, sessionmaker

metadata = sa.MetaData()
Base: Type = declarative_base(metadata=metadata)

class User(Base):
    __tablename__ = "users"
    uid = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), index=True, nullable=False, unique=True)
    email = sa.Column(sa.String(50), index=True, nullable=False, unique=True)
    password = sa.Column(sa.String(50), nullable=False)

    def __str__(self):
        return f'User(name={self.name!r}, password={self.password!r}, email={self.email!r})'


def init_db(dns: str):
    engine = sa.create_engine(dns)
    Session = sessionmaker(engine)
    metadata.create_all(engine)
    return Session
