from pprint import pprint
import core_model as tbl
import db_core_data as dat
import sqlalchemy as sa
from typing import Union
from dataclasses import asdict
from rich.console import Console
from rich.table import Table
from rich.text import Text
from sqlalchemy.exc import IntegrityError


console = Console()
conn = tbl.engine.connect()
data_type = Union[dat.product_, dat.user_, dat.order_]


def insert_data(
    conn: sa.Connection,
    table: sa.Table,
    data: list,
) -> sa.CursorResult:
    data_ = [asdict(d) for d in data]
    q = sa.insert(table).values(data_)
    return conn.execute(q)


# insert data to the database
def insert_generated_data(conn: sa.Connection):
    insert_data(conn, tbl.users, dat.sample_users)
    insert_data(conn, tbl.products, dat.sample_products)
    insert_data(conn, tbl.orders, dat.sample_orders)


def from_snake_case(name: str, sep: str = " "):
    return sep.join(n.capitalize() for n in name.split("_"))


def make_table(*titles: sa.Label | sa.Column):
    table = Table(*(from_snake_case(t.name) for t in titles))

    def render_row(row):
        return (Text(str(r)) for r in row)

    def add_rows(rows):
        for row in rows:
            r = render_row(row)
            table.add_row(*r)
        return table

    return add_rows


def print_table(cols, rows):
    t = make_table(*cols)
    console.print(t(rows))


def query_table_data(conn: sa.Connection):
    sold_prod_quantity = sa.func.sum(tbl.orders.c.quantity)
    total_prod_quantity = sold_prod_quantity + tbl.products.c.quantity
    total_achievable_price = total_prod_quantity * tbl.products.c.unit_cost
    total_sold_price = sold_prod_quantity * tbl.products.c.unit_cost
    total_instock_price = tbl.products.c.quantity * tbl.products.c.unit_cost
    cols = (
        tbl.products.c.name.label("Product Name"),
        tbl.products.c.unit_cost.label("Unit Cost"),
        tbl.products.c.quantity.label("InStock"),
        total_instock_price.label("InStock Price"),
        sold_prod_quantity.label("Sold"),
        total_sold_price.label("Sold Price"),
        total_prod_quantity.label("Total Quantity"),
        total_achievable_price.label("Total Price"),
    )
    q = (
        sa.select(*cols)
        .select_from(tbl.orders.join(tbl.products))
        .group_by(tbl.products.c.pid)
    )
    r = conn.execute(q)
    print_table(cols, r)


def query_products_table(
    conn: sa.Connection,
    *,
    product_id=True,
    product_name=True,
    unit_cost=True,
    instock_quantity=False,
    instock_cost=False,
    sold_quantity=False,
    sold_cost=False,
    total_quantity=True,
    total_cost=False,
    product_ids=None,
):
    _ids = conn.execute(sa.select(tbl.products.c.pid))
    product_ids = product_ids if product_ids is not None else [_id.pid for _id in _ids]
    sold_prod_quantity = sa.func.sum(tbl.orders.c.quantity)
    total_prod_quantity = sold_prod_quantity + tbl.products.c.quantity
    total_achievable_price = total_prod_quantity * tbl.products.c.unit_cost
    total_sold_price = sold_prod_quantity * tbl.products.c.unit_cost
    total_instock_price = tbl.products.c.quantity * tbl.products.c.unit_cost
    cols = [
        col
        for col, show in (
            (tbl.products.c.pid.label("product_id"), product_id),
            (tbl.products.c.name.label("product_name"), product_name),
            (tbl.products.c.unit_cost.label("unit_cost"), unit_cost),
            (tbl.products.c.quantity.label("instock_quantity"), instock_quantity),
            (total_instock_price.label("instock_cost"), instock_cost),
            (sold_prod_quantity.label("sold_quantity"), sold_quantity),
            (total_sold_price.label("sold_cost"), sold_cost),
            (total_prod_quantity.label("total_quantity"), total_quantity),
            (total_achievable_price.label("total_cost"), total_cost),
        )
        if show
    ]
    q = (
        sa.select(*cols)
        .select_from(tbl.orders.join(tbl.products))
        .where(sa.or_(False, *(tbl.products.c.pid == _id for _id in product_ids)))
        .group_by(tbl.products.c.pid)
    )
    r = conn.execute(q).all()
    print_table(cols, r)
    return [col.name for col in cols], r


# query_table_data(conn)
cols, rows = query_products_table(
    conn,
    product_id=True,
    product_name=True,
    unit_cost=True,
    instock_quantity=True,
    instock_cost=False,
    sold_quantity=True,
    sold_cost=False,
    total_quantity=True,
    total_cost=False,
    product_ids=(1, 3, 4, 5, 2),
)


pprint(cols)
pprint(rows)


def sql_errors(conn: sa.Connection):
    # test integrity error
    transaction = conn.begin()  # create new transaction
    user = dat.user_("Mr Simon", "simogash@gmail.com", 21)
    q = sa.insert(tbl.users).values(**asdict(user))
    try:
        r = conn.execute(q).fetchall()
        print(f"Result: {r}")
    except IntegrityError as e:
        print(e.orig)
        print(e.params)
        print(e.detail)
        print(e.statement)
    # test transaction
    try:
        r = conn.execute(q)
        print(f"Result: {r}")
        print("Commiting")
        transaction.commit()
    except IntegrityError as e:
        print(f"Rolling Back: {e.orig}")
        transaction.rollback()
    with conn.begin() as t:
        try:
            conn.execute(q)
            t.commit()
        except IntegrityError as e:
            print(f"Rolling Back After Error: {e.orig}")
            t.rollback()


# sql_errors(conn)

# insert_generated_data(conn)
# conn.commit()
