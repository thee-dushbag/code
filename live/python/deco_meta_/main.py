from typing import Any, Sequence
from dataclasses import dataclass

def AccessIF(predicate):
    def _inner_one(Class):
        def _inner_two(*args, **kwargs):
            _wrapped = Class(*args, **kwargs)
            class Wrapper:
                def __getattr__(self, _name: str) -> Any:
                    if predicate(_name): return getattr(_wrapped, _name)
                    raise Exception(f"ReadError: Access to attribute {_name!r} outside class {Class.__name__}")
                def __setattr__(self, _name: str, _value: Any) -> None:
                    if predicate(_name): return setattr(_wrapped, _name, _value)
                    raise Exception(f"WriteError: Access to attribute {_name!r} outside class {Class.__name__}")
            return Wrapper()
        return _inner_two
    return _inner_one

def Private(*privates):
    return AccessIF(lambda name: name not in privates)

def Public(*publics):
    return AccessIF(lambda name: name in publics)

@Public('name', 'setName', 'toString')
class Person:
    def __init__(self, name, email, age) -> None:
        self.name = name
        self.email = email
        self.age = age
    
    def __str__(self):
        return f'Person({self.name!r}, {self.email!r}, {self.age!r})'

    def setName(self, name):
        self.name = name

def main(argv: Sequence[str]) -> None:
    p = Person('Simon Nganga', 'simongash@gmail.com', 20)
    # p.age = 90
    p.setName('Mark John')
    print(p)
    print(__debug__)
    
if __name__ == "__main__":
    from sys import argv

    main(argv[1:])
