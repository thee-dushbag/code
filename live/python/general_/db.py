import sqlalchemy as sa
from random import randint
from pprint import pprint


def phone():
    return f"+254-7{randint(10, 99)}-{randint(100, 999)}-{randint(100, 999)}"


def qexe(connection: sa.Connection):
    def query(q, *a, **k):
        connection.execute(q, *a, **k)
        connection.commit()

    return query


metadata = sa.MetaData()
engine = sa.create_engine("sqlite:///db.sqlite")
conn = engine.connect()

users = sa.Table(
    "users",
    metadata,
    sa.Column("uid", sa.Integer(), primary_key=True),
    sa.Column("name", sa.String(30)),
    sa.Column("email", sa.String(40)),
    sa.Column("phone", sa.String(15)),
)

products = sa.Table(
    "products",
    metadata,
    sa.Column("pid", sa.Integer(), primary_key=True),
    sa.Column("name", sa.String(30)),
    sa.Column("description", sa.String(100)),
    sa.Column("unit_cost", sa.Integer(), default=0),
    sa.Column("quantity", sa.Integer(), default=1),
)

orders = sa.Table(
    "orders",
    metadata,
    sa.Column("oid", sa.Integer(), primary_key=True),
    sa.Column("pid", sa.ForeignKey("products.pid")),
    sa.Column("uid", sa.ForeignKey("users.uid")),
    sa.Column("quantity", sa.Integer(), default=1),
)

metadata.create_all(bind=engine)

sample_products = [
    dict(name="T.V", description="50 inch led T.V", unit_cost=50000, quantity=9),
    dict(
        name="D.V.D Player",
        description="Brand new vitron D.V.D player",
        unit_cost=2000,
        quantity=4,
    ),
    dict(
        name="Dining table",
        description="Light brown 3 by 1 dining table with 8 chairs.",
        unit_cost=30000,
        quantity=6,
    ),
    dict(
        name="Thermos",
        description="High pressured metallic american thermos.",
        unit_cost=800,
        quantity=15,
    ),
    dict(
        name="Coffee mug",
        description="Green-blue-artwork painted coffee mug.",
        unit_cost=400,
        quantity=23,
    ),
]

sample_users = [
    dict(name="Simon Nganga", email="simongash@gmail.com", phone=phone()),
    dict(name="Faith Njeri", email="faithnjeri@gmail.com", phone=phone()),
    dict(name="Lydia Njeri", email="lydianjeri@gmail.com", phone=phone()),
    dict(name="Darius Kimani", email="dariuskipesa@gmail.com", phone=phone()),
    dict(name="Ian Bogonko", email="ianbogonko@gmail.com", phone=phone()),
    dict(name="Edwin Kamau", email="kamauedwin@gmail.com", phone=phone()),
]

exe = qexe(conn)
# * Add products and users to the database.
q = users.insert()
exe(q, sample_users)
q = products.insert()
exe(q, sample_products)

sample_orders = [
    dict(
        uid=1,
        pid=4,
        quantity=3,
    ),
    dict(
        uid=2,
        pid=2,
        quantity=5,
    ),
    dict(
        uid=3,
        pid=2,
        quantity=5,
    ),
    dict(
        uid=6,
        pid=5,
        quantity=6,
    ),
    dict(uid=1, pid=1, quantity=5),
]
# * Adding sample orders to database.
q = orders.insert()
exe(q, sample_orders)

cols = (
    users.c.name,
    products.c.name,
    orders.c.quantity,
    products.c.unit_cost,
    orders.c.quantity * products.c.unit_cost,
)

who_ordered = (
    sa.select(*cols)
    .select_from(orders.join(products).join(users))
    .where(sa.and_(users.c.uid == orders.c.uid))
)

r = conn.execute(who_ordered)
l = 14
sep = " | "
print(
    sep
    + "User Name".ljust(l)
    + sep
    + "Product Name".ljust(l)
    + sep
    + "Quantity".ljust(l)
    + sep
    + "Unit Cost".ljust(l)
    + sep
    + "Total Price".ljust(l)
    + sep
)

for row in r:
    uname = str(row[0]).ljust(l) + sep
    pname = str(row[1]).ljust(l) + sep
    quant = str(row[2]).ljust(l) + sep
    unitc = str(row[3]).ljust(l) + sep
    total = str(row[4]).ljust(l) + sep
    print(sep + uname + pname + quant + unitc + total)


# q = orders.join(products).join(users).select().where(users.c.uid == 1)
# r = conn.execute(q)
# pprint(r.fetchall())

# cols = (users.c.name, sa.func.count(orders.c.uid))
# q = sa.select(*cols).select_from(orders.join(users)).group_by(users.c.uid)
# r = conn.execute(q)
# print(r.fetchall())

cols = (users.c.name, sa.func.sum(products.c.unit_cost * orders.c.quantity))
q = sa.select(*cols).select_from(orders.join(products).join(users)).group_by(users.c.uid)
r = conn.execute(q)
