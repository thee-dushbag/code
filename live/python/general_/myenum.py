from typing import Type

class NotFoundEnum(Exception):
    ...

class MyEnumValue:
    def __init__(self, name: "MyEnumAuto", value: int) -> None:
        self.value = value
        self.name = name

    def __str__(self) -> str:
        return f"<{self.name.name}: {self.value}>"

    def __repr__(self) -> str:
        return str(self)

class BaseEnum:
    __enum__ = 0
    __values__ = ()  # type:ignore
    __raise__ = True

    def __init__(self) -> None:
        raise Exception("Cannot Instantiate an Enum")

    def __init_subclass__(cls) -> None:
        cls._set_values()
        init = getattr(cls, "__init__", None)
        if not init == BaseEnum.__init__:
            raise Exception("Cannot Instantiate an Enum")

    @classmethod
    def string(cls) -> str:
        return f'{cls.__name__}{cls[:]}'

    @classmethod
    def _slice_class(cls, sel: slice):
        start = sel.start or 1
        stop = sel.stop or cls.__enum__ + 1
        step = sel.step or 1
        return tuple(cls[i] for i in range(start, stop, step))

    @classmethod
    def _set_values(cls):
        cls.__values__: list[MyEnumValue] = []
        for key in dir(cls):
            value = getattr(cls, key, None)
            if isinstance(value, MyEnumValue):
                cls.__values__.append(value)

    @classmethod
    def _not_found(cls, v=None):
        etext = (
            f"Enum value of {v} was not found in Enum"
            f" {cls.__name__}\nValid Enums: {cls.__values__}"
        )
        if cls.__raise__:
            raise NotFoundEnum(etext)
        not_found = MyEnumAuto()
        not_found.__set_name__(BaseEnum, "NOT_FOUND")
        value = MyEnumValue(not_found, v or -1)
        return value

    @classmethod
    def _get_item(cls, sel: int):
        for value in cls.__values__:
            if value.name.cls == cls:
                if value.value == sel:
                    return value
        return cls._not_found(sel)

    @classmethod
    def _get_str_item(cls, sel: str):
        for value in cls.__values__:
            if value.name._name == sel:
                return value
        return cls._not_found(sel)

    def __class_getitem__(cls, sel: int):
        if isinstance(sel, slice):
            return cls._slice_class(sel)
        if cls.__values__ is None:
            cls._set_values()
        if isinstance(sel, int):
            return cls._get_item(sel)
        return cls._get_str_item(str(sel))


class EV: ...

class AnnotatedBaseEnum(BaseEnum):
    @classmethod
    def _set_values(cls):
        for key, t in cls.__annotations__.items():
            if not t == EV: continue
            value = MyEnumAuto()
            value.__set_name__(cls, key)
            setattr(cls, key, value)
        super()._set_values()


class MyEnumAuto:
    def __set_name__(self, cls: Type[BaseEnum], name: str):
        cls.__enum__ += 1
        self.cls = cls
        self._name = name.lower()
        self.name = f"{cls.__name__}.{name}"
        self.value = MyEnumValue(self, cls.__enum__)  # type:ignore

    def __get__(self, inst, cls):
        print(f"Getting: {self.name} -> {self.value}")
        return self.value

    def __set__(self, inst, value):
        print(f"Setting: {self.name}={value}")
        # raise Exception(f"{self.name} is a readonly property")

    def __delete__(self, *_):
        print(f"Deletting: {self.name}")
        # raise Exception(f"Cannot delete Enum property: {self.name}")
