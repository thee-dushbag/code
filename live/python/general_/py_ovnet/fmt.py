class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    @property
    def email(self) -> str:
        username = self.name.replace(" ", "").lower()
        return username + "@gmail.com"

    def __format__(self, __format_spec: str) -> str:
        return __format_spec % {
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "ID": id(self),
            "IDX": hex(id(self)),
        }

    def __reduce__(self) -> str | tuple[object, ...]:
        return __class__, (self.name, self.age)

    def __str__(self) -> str:
        return format(self, "Person(%(name)r, %(age)r, %(email)r)")

    def __repr__(self) -> str:
        return format(
            self, "<object Person at %(IDX)s with (name=%(name)r, age=%(age)r)>"
        )

    def introduce_self(self) -> str:
        return format(
            self,
            "My name is %(name)s and I am %(age)r years old. "
            "You can contact me via my email %(email)s.",
        )

if __name__ == '__main__':
    import pickle
    me = Person("Simon Nganga", 21)
    print(me)
    print(repr(me))
    print(me.introduce_self())
    print(f"Hello {me:%(name)s}, how was your day?")
    meb = pickle.dumps(me, fix_imports=False)
    print(meb)
    me2 = pickle.loads(meb)
    print(me2)
