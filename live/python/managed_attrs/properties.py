from random import choice


def email_domain():
    prov = "gmail", "yahoo", "outlook"
    com = "com", "mil", "xyz", "ac.ke", "ku.uk"
    return f"{choice(prov)}.{choice(com)}"


class Person:
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
        return f"Person(name={self.name!r}, age={self.age}, email={self.email!r})"


class PersonName:
    def __init__(self, name: str) -> None:
        self._name = name

    def getName(self):
        print("fetching: name")
        return self._name

    def setName(self, name):
        print("setting: name")
        self._name = name

    def delName(self):
        print("forgetting: name")
        self._name = ""

    name = property(getName, setName, delName, "Name Property: Person::name")

    def __str__(self):
        return f"Name: {self.name!r}"
