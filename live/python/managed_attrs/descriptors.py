from typing import Type, Generic, TypeVar, cast
from random import choice

def email_domain():
    prov = 'gmail', 'yahoo', 'outlook'
    com = 'com', 'mil', 'xyz', 'ac.ke', 'ku.uk'
    return f'{choice(prov)}.{choice(com)}'

T = TypeVar('T')
V = TypeVar('V')
K = TypeVar('K')

FunctionSentinel = lambda *a, **k: None

class Descriptor(Generic[T, V]):
    """Descriptor Docstring"""
    def __init__(self, default_creator: Type=object) -> None:
        super().__init__()
        self.creator = default_creator
        self.value: V  = default_creator()
    
    def __set_name__(self, cls: Type[T], name: str):
        # print(f"Setting Name: {name}")
        self.name = name
    
    def __get__(self, instance: T, cls: Type[T]) -> V:
        print(f"[{self.name}]: Getting...")
        return cast(V, self.value)
    
    def __set__(self, instance: T, value: V):
        print(f"[{self.name}]: Setting...")
        self.value = value
    
    def __delete__(self, instance: T):
        print(f"[{self.name}]: Deleting...")
        self.value = self.creator()


class RestrictTypes(Generic[V, T]):
    def __init__(self, *types: Type[T]) -> None:
        self.types: tuple[Type[T]] = types or (object,)
        self.value = self.types[0]()

    def __set_name__(self, owner: Type[T], name: str):
        self.name = name

    def __get__(self, instance: T, owner: Type[V]):
        return self.value

    def __set__(self, instance: T, value: K):
        assert self._validate_types(value),\
            f"Cannot assign {self.name} value {value!r} of type {type(value)}"
        self.value = value

    def _validate_types(self, value: K):
        return issubclass(type(value), self.types)

    def __delete__(self, instance: T):
        self.value = self.types[0]()


class OneOf:
    def __init__(self, *values) -> None:
        self.possible_values = values or (None,)
        self.value = self.possible_values[0]
    
    def __set_name__(self, owner, name: str):
        self.name = name
        self.class_name = owner.__name__
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        assert value in self.possible_values, \
            f"{self.class_name}::{self.name} must be one of {self.possible_values} not {value!r}"
        self.value = value

class istr(str):
    def __eq__(self, other: str):
        return self.lower() == other.lower()

class TypeAttrs:
    name = RestrictTypes(str)
    age = RestrictTypes(int)
    gender = OneOf(istr('male'), istr('female'))


class Person:
    name = Descriptor(str)
    age = Descriptor(int)
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    @property
    def email(self):
        print(f"Fetching email value")
        return f"{self.name.replace(' ', '_').lower()}@{email_domain()}"
    
    @email.setter
    def email(self, e):
        print(f"Cannot Set New Email: {e}")
    
    def __str__(self):
        return f'Person(name={self.name!r}, age={self.age}, email={self.email!r})'
    

class PersonName:
    name = Descriptor()
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __str__(self):
        return f'PersonName({self.name!r})'

class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None) -> None:
        self.fset = fset
        self.fget = fget
        self.fdel = fdel
        self.__doc__ = doc or "Property Descriptor"
    def __set_name__(self, cls, name):
        self.name = name
    def __set__(self, instance, value):
        if self._valid(self.fset):
            return self.fset(instance, value)
        raise AttributeError("Cannot set as no setter was provided")
    def __get__(self, instance, cls):
        if self._valid(self.fget):
            return self.fget(instance)
        raise AttributeError("Cannot get as no getter was provided")
    def __delete__(self, instance):
        if self._valid(self.fdel):
            self.fdel(instance)
            return self._delete()
        raise AttributeError("Cannot delete as no deleter was provided")
    def _delete(self):
        self.fset = FunctionSentinel
        self.fget = FunctionSentinel
        self.fdel = FunctionSentinel
    @staticmethod
    def _valid(func):
        return func is FunctionSentinel or func is not None
    def setter(self, fset):
        self.fset = fset
        return self
    def getter(self, fget):
        self.fget = fget
        return self
    def deleter(self, fdel):
        self.fdel = fdel
        return self