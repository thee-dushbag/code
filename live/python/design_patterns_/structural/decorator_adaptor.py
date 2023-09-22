from typing import Any

from mypyutils.events import Event


class Object:
    def __init__(self, data: Any = None) -> None:
        self.data = data

    def show(self):
        print(f"Data: {self.data}")

    def get(self) -> Any:
        return self.data

    def set(self, data: Any = None) -> None:
        self.data = data

    def __str__(self) -> str:
        return f"<Object(data={self.data!r})>"


class MyObject(Object):
    emitter = Event()

    def __init__(self, data: Any = None) -> None:
        self.emitter.emit("Object_init")
        super().__init__(data)

    def get(self) -> Any:
        self.emitter.emit("Object_get")
        return super().get()

    def set(self, data: Any = None) -> None:
        self.emitter.emit("Object_set")
        return super().set(data)

    def __str__(self) -> str:
        self.emitter.emit("Object_str")
        return super().__str__()

    def show(self):
        self.emitter.emit("Object_show")
        return super().show()
