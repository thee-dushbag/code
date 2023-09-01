from dataclasses import dataclass
from typing import Protocol, runtime_checkable

@runtime_checkable
class NamedProtocol(Protocol):
    @property
    def __name__(self) -> str: ...

@dataclass
class Person:
    name: str
    email: str
    age: int
    @property
    def __name__(self):
        return self.name

@dataclass
class Desk:
    width: float
    height: float
    length: float
    
    @property
    def __name__(self):
        return f'Desk({self.length}*{self.width}*{self.height})'

def name(named: NamedProtocol) -> str:
    if isinstance(named, NamedProtocol):
        return named.__name__
    raise Exception(f"Object of type {type(named)} is not named.")

desk = Desk(100, 75, 50)
person = Person("Simon Nganga", "simongash@gmail.com", 20)

print(name(person))
print(name(desk))
print(name(Desk))