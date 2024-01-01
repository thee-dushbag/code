from random import randint, shuffle
from wallet import Wallet


def getprice1(price: int, money: list[int]) -> Wallet:
    # Greedy Choince Property
    money.sort()
    index = len(money)
    found = Wallet.fromkeys(money)
    while index:
        coin = money[index - 1]
        if coin <= price:
            price -= coin
            found += coin
            if price == 0:
                break
            continue
        index -= 1
    return found


def getprice2(price: int, money: list[int]) -> Wallet:
    # Optimal Substructure
    size, index = len(money), 0
    found = Wallet.fromkeys(money)
    while index < size:
        coin = money[index]
        if coin <= price:
            price -= coin
            found += coin
            if price == 0:
                break
            continue
        index += 1
    return found


money = [1, 5, 10, 20, 50, 100, 200, 500, 1000]
shuffle(money)
prices = (randint(1, 10000) for _ in range(50))

print("money=", money)
for price in prices:
    for getprice in getprice1, getprice2:
        found = getprice(price, money.copy())
        assert (
            found.total() == price
        ), f"{price} != sum({list(found.keys())}) ::: {price} != {int(found)} ::: {getprice=}"
        print(price, "->", +found)
