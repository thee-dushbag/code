import asyncio as aio
from random import randrange


class Product:
    def __init__(self, name: str, checkout_time: float):
        self.name = name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, cid: int, prods: list[Product]):
        self.cid = cid
        self.prods = prods


async def checkout_customer(queue: aio.Queue[Customer], cid: int):
    while not queue.empty():
        cust = queue.get_nowait()
        print(f"Cashier {cid} checking out customer {cust.cid}")
        for prod in cust.prods:  # B
            print(f"--> Cashier {cid} checking out customer {cust.cid}'s {prod.name}")
            await aio.sleep(prod.checkout_time)
        print(f"> Cashier {cid} finished checking out customer {cust.cid}")
        queue.task_done()


async def main():
    customers: aio.Queue[Customer] = aio.Queue()

    products: list[Product] = [
        Product("bananas", 0.5),
        Product("sausage", 0.2),
        Product("bread", 0.2),
        Product("milk", 1),
        Product("beer", 2),
    ]

    for i in range(10):
        prods = [products[randrange(len(products))] for _ in range(randrange(2, 10))]
        await customers.put(Customer(i, prods))

    cashiers = [aio.create_task(checkout_customer(customers, i)) for i in range(3)]
    await aio.gather(customers.join(), *cashiers)


if __name__ == "__main__":
    aio.run(main())
