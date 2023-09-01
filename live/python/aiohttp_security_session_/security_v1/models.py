import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

DB_KEY = 'users.database.test.site.unique'
metadata = sa.MetaData()
Base = declarative_base(metadata=metadata)

class User(Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(40), nullable=False, unique=True)
    email = sa.Column(sa.String(40), nullable=False, unique=True)
    password = sa.Column(sa.String(50), default=str())

def init_db(dns: str):
    print("Connecting to database")
    engine = sa.create_engine(dns)
    metadata.create_all(engine)
    Session = sessionmaker(engine)
    return Session