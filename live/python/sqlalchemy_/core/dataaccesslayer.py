from pprint import pprint
import sqlalchemy as sa

engine = sa.create_engine('sqlite:///db_core.sqlite3')
metadata = sa.MetaData()

# users = sa.Table('users', metadata, autoload_with=engine)
# products = sa.Table('products', metadata, autoload_with=engine)
# orders = sa.Table('orders', metadata, autoload_with=engine)

metadata.reflect(engine)
users = metadata.tables['users']

q = sa.select(users)
conn = engine.connect()
us = conn.execute(q).all()
pprint(metadata.tables.values())
pprint(us)