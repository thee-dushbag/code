from dataclasses import asdict
import db_orm_data as dat
import orm_model as tbl
import sqlalchemy as sa
from rich.console import Console
from rich.table import Table
from rich.text import Text


console = Console()
session = tbl.Session()


def insert_sample_data(session, table, data: list):
    session.add_all(table(**asdict(dat)) for dat in data)


def insert_sample_datas(session):
    insert_sample_data(session, tbl.User, dat.sample_users)
    insert_sample_data(session, tbl.Order, dat.sample_orders)
    insert_sample_data(session, tbl.Product, dat.sample_products)


##! Add data to database
# insert_sample_datas(session)
# session.commit()


def from_snake_case(name: str, sep: str = " "):
    return sep.join(n.title() for n in name.split("_"))


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


def products_query(
    session,
    *,
    pid=True,
    name=False,
    unit_cost=True,
    instock_quantity=False,
    instock_price=False,
    sold_quantity=False,
    sold_price=False,
    total_quantity=True,
    total_price=False,
    product_pids=(),
    all_cols=False,
):
    product_id = tbl.Product.pid.label("product_id")
    product_pids = product_pids or (
        r.product_id for r in session.query(product_id).all()
    )
    product_name = tbl.Product.name.label("product_name")
    product_unit_cost = tbl.Product.unit_cost.label("product_unit_cost")
    product_instock_quantity = tbl.Product.quantity.label("product_instock_quantity")
    product_instock_price = (product_instock_quantity * product_unit_cost).label(
        "product_instock_price"
    )
    product_sold_quantity = sa.func.sum(tbl.Order.quantity).label(
        "product_sold_quantity"
    )
    product_sold_price = (product_sold_quantity * product_unit_cost).label(
        "product_sold_price"
    )
    product_total_quantity = (product_sold_quantity + product_instock_quantity).label(
        "product_total_quantity"
    )
    product_total_price = (product_total_quantity * product_unit_cost).label(
        "product_total_price"
    )
    cols = [
        col
        for col, include in (
            (product_id, pid),
            (product_name, name),
            (product_unit_cost, unit_cost),
            (product_instock_quantity, instock_quantity),
            (product_instock_price, instock_price),
            (product_sold_quantity, sold_quantity),
            (product_sold_price, sold_price),
            (product_total_quantity, total_quantity),
            (product_total_price, total_price),
        )
        if include or all_cols
    ]
    rows = (
        session.query(*cols)
        .select_from(sa.join(tbl.Order, tbl.Product))
        .where(sa.or_(False, *(tbl.Product.pid == pid_ for pid_ in product_pids)))
        .group_by(tbl.Product.pid)
    )
    return cols, rows


##! Query all data about the products
# cols, rows = products_query(session, all_cols=True, product_pids=(6, 7))
# print_table(cols, rows)


def orders_query(
    session,
    *,
    oid=True,
    uid=False,
    uname=True,
    pid=False,
    pname=True,
    unit_cost=True,
    quantity=True,
    price=True,
    all_cols=False,
):
    order_id = tbl.Order.oid.label("order_id")
    user_id = tbl.Order.uid.label("user_id")
    user_name = tbl.User.name.label("user_name")
    product_id = tbl.Order.pid.label("product_id")
    product_name = tbl.Product.name.label("product_name")
    product_unit_cost = tbl.Product.unit_cost.label("product_unit_cost")
    order_quantity = tbl.Order.quantity.label("order_quantity")
    order_price = (order_quantity * product_unit_cost).label("order_price")
    cols = [
        col
        for col, include in (
            (order_id, oid),
            (user_id, uid),
            (user_name, uname),
            (product_id, pid),
            (product_name, pname),
            (product_unit_cost, unit_cost),
            (order_quantity, quantity),
            (order_price, price),
        )
        if include or all_cols
    ]

    rows = (
        session.query(*cols)
        .select_from(sa.join(tbl.Order, tbl.User).join(tbl.Product))
        .group_by(tbl.Order.oid)
    )
    return cols, rows


def user_order(
    session,
    uid: int,
    *,
    oid=True,
    pid=False,
    pname=False,
    unit_cost=True,
    quantity=True,
    price=True,
    all_cols=False,
):
    cols, rows = orders_query(
        session,
        oid=oid or all_cols,
        uid=False,
        uname=False,
        pid=pid or all_cols,
        pname=pname or all_cols,
        unit_cost=unit_cost or all_cols,
        quantity=quantity or all_cols,
        price=price or all_cols,
    )
    return cols, rows.filter(tbl.User.uid == uid)


def product_order(
    session,
    pid: int,
    *,
    oid=True,
    uid=False,
    uname=False,
    quantity=True,
    price=True,
    all_cols=False,
):
    cols, rows = orders_query(
        session,
        oid=oid or all_cols,
        uid=uid or all_cols,
        uname=uname or all_cols,
        pname=False,
        pid=False,
        unit_cost=False,
        quantity=quantity or all_cols,
        price=price or all_cols,
    )
    return cols, rows.filter(tbl.Product.pid == pid)


def users_order_query(
    session,
    *,
    uid=True,
    name=False,
    order_count=True,
    total_order_quantity=True,
    total_order_price=True,
    all_cols=False,
):
    user_id = tbl.User.uid.label("user_id")
    user_name = tbl.User.name.label("user_name")
    user_total_item_quantity = sa.func.sum(tbl.Order.quantity).label(
        "user_total_item_quantity"
    )
    total_order_count = sa.func.count(tbl.Order.uid).label("total_order_count")
    user_total_order_price = sa.func.sum(
        tbl.Product.unit_cost * tbl.Order.quantity
    ).label("user_total_order_price")
    cols = [
        col
        for col, include in (
            (user_id, uid),
            (user_name, name),
            (total_order_count, order_count),
            (user_total_item_quantity, total_order_quantity),
            (user_total_order_price, total_order_price),
        )
        if include or all_cols
    ]
    rows = (
        session.query(*cols)
        .select_from(sa.join(tbl.Order, tbl.User).join(tbl.Product))
        .group_by(tbl.User.uid)
    )
    return cols, rows


##! Query all data about the users
# cols, rows = users_order_query(session)
# print_table(cols, rows)
# cols, rows = orders_query(session, uid=True, pid=True)
# rows = rows.filter(tbl.Order.uid == 2)
# cols, rows = user_order(session, 2, pid=True, pname=True)
# print_table(cols, rows)
# cols, rows = product_order(session, 6, uname=True)
# cols, rows = orders_query(session, uname=False, pname=False, unit_cost=False)
# rows = rows.filter(tbl.User.uid == 2).filter(tbl.Product.pid == 4)
# print_table(cols, rows)

# cols, rows = products_query(
#     session,
#     product_pids=(6,),
#     pid=False,
#     total_quantity=False,
#     unit_cost=False,
#     total_price=False,
#     sold_price=True,
# )
# price = rows.scalar()
# print(f"Total sold price of Coffe mugs: {price}")
# print_table(cols, rows)