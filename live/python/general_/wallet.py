class Wallet(dict[int, int]):
    def total(self) -> int:
        return sum(m * self[m] for m in self)

    def pop(self, money: int, count: int = 1):
        if self[money] < count:
            raise ValueError(
                "Overwithdraw encountered. Tried to remove"
                f" {count} {money}'s where {self[money]} exist."
            )
        self[money] -= count
        return self[money]

    def add(self, money: int, count: int = 1):
        self[money] += count
        return self[money]

    def __iadd__(self, money):
        self.add(money)
        return self

    def __isub__(self, money):
        self.pop(money)
        return self

    def real(self) -> dict[int, int]:
        return {money: count for money, count in self.items() if count > 0}

    def imag(self) -> dict[int, int]:
        return {money: count for money, count in self.items() if count <= 0}

    __pos__, __neg__ = real, imag
    __bool__ = __int__ = total

    @classmethod
    def fromkeys(cls, money):
        return cls({m: 0 for m in money})

    def count(self, money: int) -> int:
        return self[money]

    def __contains__(self, money: int) -> bool:
        return self.count(money) > 0
