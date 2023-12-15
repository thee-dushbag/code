import json as js
from itertools import chain
from random import choice, randint
from typing import Sequence

import sqlalchemy as sa
from pydantic import BaseModel, EmailStr, Field
from rich.console import Console
from rich.table import Table
from rich.text import Text
from sqlalchemy.orm import declarative_base, sessionmaker

console = Console()


Base = declarative_base()
engine = sa.create_engine("sqlite:///db.sqlite")
Session = sessionmaker(bind=engine)


def mcounter(start: int, step: int = 1):
    def _count():
        nonlocal start
        start += step
        return start

    return _count


class order(BaseModel):
    uid: int
    pid: int
    quantity: int = 1
    oid: int = Field(default_factory=mcounter(0))


class product(BaseModel):
    name: str
    unit_cost: float
    quantity: int = 1
    description: str = ""
    pid: int = Field(default_factory=mcounter(0))


class user(BaseModel):
    name: str
    password: str
    phone: str = ""
    email: EmailStr = EmailStr("email@example.org")
    uid: int = Field(default_factory=mcounter(0))


def place_random_order(prods: list[product], usrs: list[user]) -> order:
    prod, usr = choice(prods), choice(usrs)
    quan = randint(0, prod.quantity)
    prod.quantity -= quan
    return order(uid=usr.uid, pid=prod.pid, quantity=quan)


class users(Base):
    __tablename__ = "users"
    uid = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(15), nullable=False)
    password = sa.Column(sa.String(30), nullable=False)
    email = sa.Column(sa.String(60))
    phone = sa.Column(sa.String(15))

    def __str__(self):
        return f"users(uid={self.uid}, name={self.name!r} password={self.password!r} email={self.email!r}, phone={self.phone!r})"


class products(Base):
    __tablename__ = "products"
    pid = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(15), nullable=False)
    description = sa.Column(sa.String(255))
    quantity = sa.Column(sa.Integer(), default=1)
    unit_cost = sa.Column(sa.Numeric(12, 2), nullable=False)

    def __str__(self):
        return f"products(pid={self.pid}, name={self.name!r} description={self.description!r} quantity={self.quantity}, unit_cost={self.unit_cost})"


class orders(Base):
    __tablename__ = "orders"
    oid = sa.Column(sa.Integer(), primary_key=True)
    quantity = sa.Column(sa.Integer(), default=1)
    uid = sa.Column(sa.Integer(), sa.ForeignKey("users.uid"))
    pid = sa.Column(sa.Integer(), sa.ForeignKey("products.pid"))

    def __str__(self):
        return f"orders(oid={self.oid}, uid={self.uid} pid={self.pid} quantity={self.quantity})"


Base.metadata.create_all(bind=engine)


def init_db(session):
    with open("data.json") as file:
        data = js.load(file)
    sample_products = [product(**p) for p in data["products"]]
    sample_users = [user(**u) for u in data["users"]]
    sample_orders = [
        ordr
        for ordr in (
            place_random_order(sample_products, sample_users) for _ in range(10)
        )
        if ordr.quantity != 0
    ]
    for sample in chain(sample_orders, sample_products, sample_users):
        if isinstance(sample, user):
            session.add(users(**sample.dict()))
        elif isinstance(sample, product):
            session.add(products(**sample.dict()))
        elif isinstance(sample, order):
            session.add(orders(**sample.dict()))
    session.commit()


def main(argv: Sequence[str]) -> None:
    session = Session()
    pname = products.name.label("Product Name")
    uname = users.name.label("User Name")
    ucost = products.unit_cost.label("Unit Cost")
    quant = orders.quantity.label("Quantity")
    total = (ucost * quant).label("Total Price")
    item_fq = sa.func.sum(orders.quantity).label("Item Frequency")
    order_fq = sa.func.count(orders.quantity).label("Order Frequency")

    cols = uname, pname, ucost, quant, total
    q = session.query(*cols)
    rs = q.join(products).join(users).order_by(sa.desc(total))
    table = Table(*(c.name for c in cols))
    for row in rs:
        rrow = [Text(str(v)) for v in row]
        table.add_row(*rrow)
    console.print(table)

    total_sum = sa.func.sum(total).label("Total Price")

    cols = uname, item_fq, order_fq, total_sum
    q = session.query(*cols)
    rs = q.join(users).join(products).group_by(users.uid).order_by(sa.desc(item_fq))
    table = Table(*[col.name for col in cols])
    for row in rs:
        rrow = [Text(str(v)) for v in row]
        table.add_row(*rrow)
    console.print(table)


if __name__ == "__main__":
    from sys import argv

    main(argv[1:])
