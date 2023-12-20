import asyncio as aio
from random import randrange, random

def counter(start: int = 0, step: int = 1):
    while True:
        yield start
        start += step

class Product:
    def __init__(self, name: str, ctime: float):
        self.name = name
        self.ctime = ctime


products: list[Product] = [
    Product("bananas", 0.5),
    Product("sausage", 0.2),
    Product("bread", 0.2),
    Product("milk", 1),
    Product("beer", 1.5),
]


class Customer:
    def __init__(self, cid, prods):
        self.cid = cid
        self.prods = prods


async def checkout_customer(queue: aio.Queue[Customer], cid: int):
    while cust := await queue.get():
        print(f"Cashier {cid} " f"checking out customer " f"{cust.cid}")
        for product in cust.prods:
            print(f"Cashier {cid} checking out customer {cust.cid}'s {product.name}")
            await aio.sleep(product.ctime)
        print(f"Cashier {cid} " f"finished checking out customer " f"{cust.cid}")
        queue.task_done()


def generate_customer(cid: int) -> Customer:
    prods = [products[randrange(len(products))] for _ in range(randrange(10))]
    return Customer(cid, prods)


async def customer_generator(queue: aio.Queue):
    for cid in counter():
        customer = generate_customer(cid)
        print("Waiting to put customer in line...")
        await queue.put(customer)
        print("Customer put in line!")
        await aio.sleep(random())


async def main():
    customers = aio.Queue(5)
    customer_producer = aio.create_task(customer_generator(customers))
    cashiers = [aio.create_task(checkout_customer(customers, i)) for i in range(3)]
    await aio.gather(customer_producer, *cashiers)


if __name__ == "__main__":
    try:
        aio.run(main())
    except KeyboardInterrupt:
        ...
