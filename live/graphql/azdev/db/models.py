import sqlalchemy as sa
from sqlalchemy import orm

Base = orm.declarative_base()

class User(Base):
    __tablename__ = 'users'

class Approach(Base):
    __tablename__ = 'approach'

class Task(Base):
    __tablename__ = 'tasks'