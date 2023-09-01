from typing import Any, Sequence
from pydantic import BaseModel, EmailStr, Field
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
import json as js
from random import choice, randint
from rich.table import Table
from rich.text import Text
from rich.console import Console


console = Console()
Base = declarative_base()
engine = sa.create_engine("sqlite:///shopping.db")
Session = sessionmaker(engine)


class User(Base):
    __tablename__ = "users"
    uid = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(15), nullable=False)
    password = sa.Column(sa.String(30), nullable=False)
    email = sa.Column(sa.String(30), nullable=False)
    phone = sa.Column(sa.String(30), nullable=False)


class Product(Base):
    __tablename__ = "products"
    pid = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(15), nullable=False)
    description = sa.Column(sa.String(100))
    quantity = sa.Column(sa.Integer(), default=1)
    unit_cost = sa.Column(sa.Numeric(6, 2), nullable=False)


class Order(Base):
    __tablename__ = "orders"
    oid = sa.Column(sa.Integer(), primary_key=True)
    uid = sa.Column(sa.Integer(), sa.ForeignKey("users.uid"))
    pid = sa.Column(sa.Integer(), sa.ForeignKey("products.pid"))
    quantity = sa.Column(sa.Integer(), default=1)


Base.metadata.create_all(engine)


def mcounter(start, step=1):
    def _counter():
        nonlocal start
        start += step
        return start

    return _counter


class product_(BaseModel):
    pid: int = Field(default_factory=mcounter(0))
    name: str
    unit_cost: float
    quantity: int = 1
    description: str | None = None


class user_(BaseModel):
    uid: int = Field(default_factory=mcounter(0))
    name: str
    password: str
    email: EmailStr
    phone: str


class order_(BaseModel):
    oid: int = Field(default_factory=mcounter(0))
    uid: int
    pid: int
    quantity: int


def place_orders(
    users: list[user_], products: list[product_], count: int = 10
) -> list[order_]:
    orders: list[order_] = []
    cnt, lmt = 0, count * 2
    while (cur := len(orders)) != count:
        print(f"Order at {cur=} to {count=} | {cnt}/{lmt}")
        user = choice(users)
        product = choice(products)
        quan = randint(0, int(product.quantity / 4) * 3)
        product.quantity -= quan
        cnt += 1
        if cnt >= lmt:
            break
        if not quan:
            continue
        order = order_(uid=user.uid, pid=product.pid, quantity=quan)
        orders.append(order)
    return orders


def add_data_to_database(session):
    with open("data.json") as file:
        data = js.load(file)
    sample_users = [user_(**u) for u in data["users"]]
    sample_products = [product_(**u) for u in data["products"]]
    sample_orders = place_orders(sample_users, sample_products, 50)
    for user in (User(**d.dict()) for d in sample_users):
        session.add(user)
    for product in (Product(**d.dict()) for d in sample_products):
        session.add(product)
    for order in (Order(**d.dict()) for d in sample_orders):
        session.add(order)


def tablize(*titles: str):
    table = Table(*titles)

    def _table(rows: Sequence[Sequence[Any]]):
        for row in rows:
            table.add_row(*(Text(str(r)) for r in row))
        return table

    return _table


def get_order_cols():
    order_id = Order.oid.label("Order ID")
    user_id = User.uid.label("User ID")
    product_id = Product.pid.label("Product ID")
    order_quan = Order.quantity.label("Quantity")
    return order_id, product_id, user_id, order_quan


def get_col_names(*cols: sa.Column | Any) -> list[str]:
    return [col.name for col in cols]


def get_product_cols():
    product_id = Product.pid.label("Product ID")
    product_name = Product.name.label("Product Name")
    product_desc = Product.description.label("Description")
    product_quan = Product.quantity.label("Quantity")
    product_uc = Product.unit_cost.label("Unit Cost")
    return product_id, product_name, product_desc, product_quan, product_uc


def get_user_cols():
    user_id = User.uid.label("User ID")
    user_name = User.name.label("User Name")
    user_email = User.email.label("User Email")
    user_pass = User.password.label("Password")
    user_phone = User.phone.label("Phone")
    return user_id, user_name, user_email, user_pass, user_phone


def main(argv: list[str]) -> None:
    session = Session()
    # add_data_to_database(session)
    # if input("Commit db: [y/n]") == 'y':
    #    session.commit()

    user_cols = get_user_cols()
    query = session.query(*user_cols).all()
    user_table = tablize(*get_col_names(*user_cols))
    t = user_table(query)
    # console.print(t)

    order_cols = get_order_cols()
    product_cols = get_product_cols()
    total_col = (product_cols[-1] * order_cols[-1]).label("Total Price")
    t_cols = (
        user_cols[1],
        product_cols[1],
        product_cols[-1],
        order_cols[-1],
        total_col,
    )
    sum_table = tablize(*get_col_names(*t_cols))
    query = session.query(*t_cols)
    query = query.join(User).join(Product).order_by(total_col).all()
    t = sum_table(query)
    # console.print(t)

    product_ordered_fq = sa.func.sum(order_cols[-1]).label("No. of Products Ordered")
    product_total_price = (product_ordered_fq * product_cols[-1]).label(
        "Ordered Stock Price"
    )
    product_stock_price = (product_cols[-1] * product_cols[-2]).label("In Stock Price")
    product_total_aprice = (product_stock_price + product_total_price).label(
        "Total Achivable Price"
    )
    t_cols = (
        product_cols[1],
        product_ordered_fq,
        product_cols[-2].label("In Stock"),
        product_cols[-1],
        product_total_price,
        product_stock_price,
        product_total_aprice,
    )
    sum_table = tablize(*get_col_names(*t_cols))
    query = (
        session.query(*t_cols)
        .join(Product)
        .group_by(product_cols[0])
        .order_by(sa.desc(product_total_price))
        .all()
    )
    t = sum_table(query)
    # console.print(t)

    product_ordered_fq = sa.func.sum(order_cols[-1]).label("Quantity")
    total_ordered_price = (product_ordered_fq * product_cols[-1]).label(
        "Ordered Stock Price"
    )
    total_stock_price = (product_cols[-2] * product_cols[-1]).label("Stock Price")
    total_price = (total_stock_price + total_ordered_price).label("Total Price")
    t_cols = (total_ordered_price, total_stock_price, total_price)
    t = tablize(*get_col_names(*t_cols))
    query = session.query(*t_cols).join(Order).all()
    # console.print(t(query))


if __name__ == "__main__":
    from sys import argv

    main(argv[1:])
