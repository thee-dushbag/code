from typing import Any


class Ops:
    def __init__(self, value) -> None:
        self.value = value

    def __getattribute__(self, __name: str) -> Any:
        print(f"[__getattribute__]: Getting: {__name}")
        return object.__getattribute__(self, __name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        print(f"[__setattr__]: Setting: {__name} -> {__value!r}")
        self.__dict__[__name] = __value

    def __delattr__(self, __name: str) -> None:
        print(f"[__delattr__]: Deleting: {__name}")

    def __getattr__(self, __name: str) -> Any:
        print(f"[__getattr__]: Getting: {__name}")
        if __name == "noexist":
            return "NoExist Attribute Value"
        raise AttributeError
