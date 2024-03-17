class metaA(type):
    def __new__(cls, name: str, bases: tuple[type, ...], kwargs: dict, *, value: int):
        return type.__new__(cls, name, bases, kwargs)

    def __init__(self, name: str, bases: tuple[type, ...], kwargs: dict, *, value: int):
        self.value = value

    def __str__(self) -> str:
        return f"<instance of metaA({self.value})>"


class instA(metaclass=metaA, value=56):
    def __init__(self, value: int) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"<instance of instA({self.value})>"


insta = instA(90)
metai = metaA("", (), {}, value=67)
print(metai)
print(metaA)
print(insta)
