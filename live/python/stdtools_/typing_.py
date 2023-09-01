from typing import Sequence
from typing import TypedDict


class Person(TypedDict, total=False):
    name: str
    email: str
    age: int


def main(argv: Sequence[str]) -> None:
    me = Person()
    me['name'] = 'Simon Nganga'
    me['age'] = 21
    me['hehe'] = 90
    print(me)


if __name__ == '__main__':
    from sys import argv
    main(argv[1:])