from typing import Optional, Type
from attrs import define, field
import sqlalchemy as sa
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    Session as _Session,
    relationship,
    backref
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.util import (
    hybridproperty,
    hybridmethod
)

Base: Type = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.Integer, primary_key=True)
    user_name = sa.Column(sa.String, index=True, nullable=False)
    user_string_emails: list[str] = association_proxy('user_emails', 'email_address')

    @hybridproperty
    def string_emails(self) -> list[str]:
        return [str(email.email_address) for email in self.user_emails]

    def __repr__(self) -> str:
        return f'User({self.user_id}, {self.user_name!r})'

class Emails(Base):
    __tablename__ = 'emails'
    email_id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.user_id))
    email_address = sa.Column(sa.String, nullable=False, unique=True)
    user = relationship('Users', backref=backref('user_emails', order_by=email_id))

    def __repr__(self) -> str:
        return f'Email({self.email_id}, {self.user_id}, {self.email_address!r})'

def get_user_emails(ses: '_Session', uid: int) -> list[Emails]:
    return ses.query(Emails).where(Emails.user_id == uid).all()

class SessionContext:
    def __init__(self, db: 'Database', commit=None) -> None:
        self.db = db
        self.commit = commit

    def __enter__(self):
        self.session = self.db.create_session()
        return self
    
    def __exit__(self, *_):
        if self.session:
            if self.commit:
                self.session.commit()
            self.session.close()

@define
class Database:
    engine: sa.engine.Engine
    metadata: sa.MetaData
    base: Type
    session_maker: sessionmaker

    def create_session(self) -> _Session:
        return self.session_maker()
    
    def with_session(self):
        return SessionContext(self)

def init_database(dns: str):
    engine = sa.create_engine(dns)
    metadata: sa.MetaData = Base.metadata
    metadata.create_all(engine)
    Session = sessionmaker(engine)
    return Database(engine, metadata, Base, Session)