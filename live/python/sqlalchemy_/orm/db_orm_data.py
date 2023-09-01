from dataclasses import dataclass, field, asdict
from random import choice, randint
from math import floor
from pydantic import BaseModel, Field, EmailStr


def mrange_id(start: int = 0, step: int = 1):
    def _next():
        nonlocal start, step
        start += step
        return start

    return _next


@dataclass
class product_:
    name: str
    unit_cost: float
    quantity: int
    description: str | None = None
    pid: int = field(default_factory=mrange_id())


@dataclass
class order_:
    uid: int
    pid: int
    quantity: int
    oid: int = field(default_factory=mrange_id())


@dataclass
class user_:
    name: str
    email: str
    age: int
    uid: int = field(default_factory=mrange_id())


products_dicts = [
    {
        "name": "T.V",
        "description": "50 inch television",
        "unit_cost": 32000.50,
        "quantity": 13,
    },
    {
        "name": "Table",
        "description": "1m diagonal brown table",
        "unit_cost": 7500,
        "quantity": 21,
    },
    {
        "name": "Office Chair",
        "description": "black cotton sponged office chair",
        "unit_cost": 5500,
        "quantity": 15,
    },
    {
        "name": "Thermos",
        "description": "2litre green thermos",
        "unit_cost": 800,
        "quantity": 35,
    },
    {
        "name": "Bed",
        "description": "3 by 5 double decker bed",
        "unit_cost": 9000,
        "quantity": 17,
    },
    {
        "name": "Coffee Mugs",
        "description": "0.8litre brown-green coffee mug",
        "unit_cost": 450,
        "quantity": 26,
    },
    {
        "name": "Office Desk",
        "description": "1m by 0.4m white office desk",
        "unit_cost": 8000,
        "quantity": 12,
    },
    {
        "name": "Gas Cooker",
        "description": "small cylinder meko cooker full gas",
        "unit_cost": 1700,
        "quantity": 24,
    },
]


user_dicts = [
    {"name": "Simon Nganga", "age": 21, "email": "simongash@gmail.com"},
    {"name": "Darius Kimani", "age": 34, "email": "dariuskimani@hotmail.com"},
    {"name": "Obed Chulo", "age": 22, "email": "obedchulo@yahoo.com"},
    {"name": "Harrisson Kariuki", "age": 19, "email": "harriskariuki@outlook.com"},
    {"name": "Faith Njeri", "age": 18, "email": "faithnjeri@gmail.com"},
    {"name": "Lydia Wanjiru", "age": 36, "email": "lydiawanjiru@hotmail.com"},
    {"name": "Judith Njeri", "age": 24, "email": "judithnjeri@gmail.com"},
    {"name": "Steve Mireri", "age": 40, "email": "stevemireri@gmail.com"},
    {"name": "Eric Omondi", "age": 25, "email": "ericomosh@gmail.com"},
    {"name": "Chris Otieno", "age": 28, "email": "chrisotish@gmail.com"},
]


def place_random_orders(
    order_count: int, users: list[user_], products: list[product_], seed: float = 0.5
) -> list[order_]:
    orders, track, max_ = [], 0, order_count * 3
    while len(orders) < order_count:
        track += 1
        product = choice(products)
        user = choice(users)
        quantity = randint(0, floor(product.quantity * seed))
        product.quantity -= quantity
        if track >= max_:
            break
        if not quantity:
            continue
        orders.append(order_(user.uid, product.pid, quantity))
    return orders


sample_products = [product_(**prod) for prod in products_dicts]
sample_users = [user_(**u) for u in user_dicts]
sample_orders = place_random_orders(50, sample_users, sample_products, seed=0.3)
