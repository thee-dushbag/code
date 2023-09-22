class StaticMethod:
    def __init__(self, function) -> None:
        self.function = function

    def __get__(self, inst, cls):
        return self.function


class ClassMethod:
    def __init__(self, function) -> None:
        self.function = function
        self.class_ = None

    def __set_name__(self, cls, name):
        self.name = name
        self.class_ = cls

    def __get__(self, inst, cls):
        if self.class_ is None:
            raise TypeError(f"{self.function!r} is not a method.")

        def dispatch(*args, **kwargs):
            return self.function(cls, *args, **kwargs)

        return dispatch


class Property:
    def __init__(self, fget=None, fset=None, fdel=None) -> None:
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, inst, cls):
        if self.fget:
            return self.fget(inst)
        raise TypeError(f"Cannot get this attribute.")

    def __set__(self, inst, value):
        if self.fset:
            return self.fset(inst, value)
        raise TypeError(f"Cannot set this attribute.")

    def __delete__(self, inst):
        if self.fdel:
            return self.fdel(inst)
        raise TypeError(f"Cannot delete this attribute.")

    def getter(self, function):
        self.fget = function
        return self

    def setter(self, function):
        self.fset = function
        return self

    def deleter(self, function):
        self.fdel = function
        return self


class Test:
    def __init__(self, name, email) -> None:
        self._name = name
        self._email = email

    @StaticMethod
    def h():
        print("Static Method: No Self, No Class")

    @ClassMethod
    def classy(cls):
        print(f"Class Method: {cls=}")

    def __str__(self) -> str:
        return f"<Test(name={self._name!r}, email={self._email!r})>"

    def emailGetter(self):
        return self._email

    def emailSetter(self, value):
        self._email = value

    def emailDeleter(self):
        self._email = None

    @Property
    def name(self):  # type: ignore
        return self._name

    # name = Property()

    @name.setter
    def name(self, value):  # type: ignore
        self._name = value

    @name.deleter
    def name(self):
        self._name = None

    email = Property(emailGetter, emailSetter, emailDeleter)


test = Test("Mark Njoroge", "simongash@gmail.com")
print("Original State:")
print(test)
print(test.name)
print(test.email)
print("Setting New Values for Name and Email:")
test.name = "Simon Nganga"
test.email = "marknjosh@yahoo.mail"
print(test)
print(test.name)
print(test.email)
print("Deleting Values for Name and Email:")
del test.name
del test.email
print(test)
print(test.name)
print(test.email)
