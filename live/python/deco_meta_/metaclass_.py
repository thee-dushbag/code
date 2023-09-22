from inspect import isclass
from typing import Any, Type

from attrs import define


class MyFirstMeta(type):
    def __new__(cls, class_name: str, bases: tuple, attrs: dict):
        print(f"Creating Class: {class_name}({bases if bases else ''}) with attrs:")
        for k, v in attrs.items():
            print(f"  {k:>18} = {v}")
        attrs["say_hi"] = cls.say_hi_meta
        attrs["metaclass"] = cls
        return type(class_name, bases, attrs)

    def say_hi_meta(self):
        return "What you looking at!!!"


class SimplestMetaclass(type):
    def __new__(cls, class_name, bases, attrs):
        print(f"In SimplestMetaclass[__new__]: {class_name}")
        return type.__new__(cls, class_name, bases, attrs)

    def __init__(self, class_name, bases, attrs):
        print(f"In SimplestMetaclass[__init__]: {class_name}")
        self.class_name = class_name
        self.method = self.METHOD
        state = " " if isclass(self) else " not a "
        print(f"self: -> {self}: is{state}class")

    def METHOD(self):
        print("This method is from SimplestMetaclass")


def _is_type(func: Any) -> Type[Any]:
    return func


@_is_type
def MetaFunc(
    class_name: str, bases: tuple[Type, ...], attrs: dict[str, Any]
) -> Type[Any]:
    print(f"Creating class: {class_name} from MetaFunc")
    clas = type(class_name, bases, attrs)
    clas.class_name = class_name
    clas.method = lambda self: print(f"MetaFunc method attached: {self}")
    return clas


# @define(slots=True)
# class Person(metaclass=MyFirstMeta):
#     name: str
#     email: str
#     age: int

#     def say_hi(self):
#         return f"Hello {self.name}, how was your day?"


# class MetaClassCall(type):
#     def __new__(cls: Type, class_name, bases, attrs) -> Type[Any]:
#         print(f'MetaClassCall.__new__[{class_name}]')
#         return type.__new__(cls, class_name, bases, attrs)

#     def __call__(cls: Type, class_name, bases, attrs) -> Type[Any]:
#         print(f'MetaClassCall.__call__[{class_name}]')
# return type.__new__(cls, class_name, bases, attrs)

# class SubMetaClassCall(type, metaclass=MetaClassCall):
#     def __call__(cls, class_name, bases, attrs) -> Type:
#         print(f'SubMetaClassCall.__call__[{class_name}]')
#         return type(class_name, bases, attrs)

# class MetaclassInheritance(type):
#     def __new__(cls: Type, class_name, bases, attrs) -> Type[Any]:
#         print(f'MetaclassInheritance.__new__[{class_name}]')
#         cls.__init_subclass__ = cls._init_subclass
#         return type.__new__(cls, class_name, bases, attrs)

#     def __init__(self, class_name, bases, attrs):
#         self.__init_subclass__ = self._init_subclass

#     def _init_subclass(self, *args, **kwargs):
#         raise Exception(f"Cannot inherit from: {self}")

# class WrapperMetaclass(metaclass=MetaclassInheritance):
#     def __init__(self) -> None:
#         print("Wrapper class init")

#     def __init_subclass__(cls) -> None:
#         print(f"{cls} is inheriting from WrapperMetaclass")

# class SimpleClass(WrapperMetaclass):
#     def __init__(self) -> None:
#         super().__init__()
#         print('SimpleClass class init')


def Tracer(aClass):
    class Wrapper:
        def __init__(self, *a, **k) -> None:
            self.wrapped = aClass(*a, **k)

        def __getattr__(self, __name: str) -> Any:
            print(f"Trace: {__name}")
            return getattr(self.wrapped, __name)

    return Wrapper


@_is_type
def MetaTracer(classname: str, bases: tuple[Type, ...], attrs: dict[str, Any]) -> Type:
    aClass = type(classname, bases, attrs)
    return Tracer(aClass)


# @Tracer
class Person(metaclass=MetaTracer):
    def __init__(self, name, hours, rate):
        self.name = name
        self.hours = hours
        self.rate = rate

    def pay(self):
        return self.hours * self.rate
