import sqlalchemy as sa
from db_orm import print_table, users_order_query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import AutomapBase, automap_base
from sqlalchemy.orm import sessionmaker

engine: sa.Engine = sa.create_engine("sqlite:///db.sqlite3", echo=False)
Base: AutomapBase = automap_base()
Session = sessionmaker(engine)
Base.prepare(engine)
session = Session()

print(Base.classes.keys())

users = Base.classes.users
orders = Base.classes.orders
products = Base.classes.products

cols, rows = users_order_query(session, uid=False, name=True)
print_table(cols, rows)
cols = (users.name, users.email, users.age)  # type: ignore
rows = session.query(*cols)
print_table(cols, rows)
user = users(name="Mark Njoroge Njenga", email="marknjoroge@gmail.com", age=2)

try:
    session.commit()
except IntegrityError as e:
    session.rollback()
    print(f"User Not Added: {e.orig}")
else:
    print("User Added")

session.close()
