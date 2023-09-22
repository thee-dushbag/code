import enum as _enum

import attrs as _attrs


def flag_on(value: int, flag: int) -> int:
    return value | flag


def flag_off(value: int, flag: int) -> int:
    return value ^ flag


def flag_enabled(value: int, flag: int) -> bool:
    return (value & flag) == flag


def flag_disabled(value: int, flag: int) -> bool:
    return not flag_enabled(value, flag)


class perm(_enum.IntFlag):
    execute = _enum.auto()
    write = _enum.auto()
    read = _enum.auto()

    @classmethod
    def interpret(cls, perm: int):
        return {
            name: flag_enabled(perm, int(flag))
            for name, flag in cls.__members__.items()
        }


@_attrs.define
class Person:
    name: str
    perm: int

    def status(self):
        perms = perm.interpret(self.perm)
        granted, denied = [], []
        for p, v in perms.items():
            if v:
                granted.append(p)
            else:
                denied.append(p)
        print("-" * 50)
        print(f"Name: {self.name}")
        print("Permissions:")
        print(f"\tGranted: {', '.join(granted)}")
        print(f"\tDenied: {', '.join(denied)}")
        print("-" * 50)

    def grant(self, _perm: int):
        self.perm = flag_on(self.perm, _perm)

    def deny(self, _perm: int):
        self.perm = flag_off(self.perm, _perm)

    def can(self, _perm: int):
        return flag_enabled(self.perm, _perm)

    def cannot(self, _perm: int):
        return flag_disabled(self.perm, _perm)


me = Person("Simon Nganga", 6)
me.status()
me.grant(perm.read | perm.execute)
me.status()
me.deny(perm.write | perm.read)
me.status()
print(f"Can I read: {me.can(perm.read)}")
print(f"Can I execute: {me.can(perm.execute)}")
print(f"I can't read: {me.cannot(perm.read)}")
print(f"I can't read and write: {me.cannot(perm.read | perm.write)}")
print(
    f"I can't read and write and execute: {me.cannot(perm.read | perm.write | perm.execute)}"
)
