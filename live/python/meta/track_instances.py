import typing as ty


T = ty.TypeVar("T")
Bases = tuple[type, ...]


def __object_new__(klass, *_, **__):
    return object.__new__(klass)


P = ty.ParamSpec("P")


class TrackInstances(type):
    all_instances: dict["TrackInstances", set] = {}

    def __new__(cls, name: str, bases: Bases, attrs: dict):
        new_meth = attrs.get("__new__", __object_new__)
        attrs["__new__"] = cls._wrap_new(new_meth)
        return super().__new__(cls, name, bases, attrs)

    def __init__(self, n: str, b: Bases, a: dict):
        self.instances: set = set()
        self.all_instances[self] = self.instances

    @classmethod
    def _wrap_new(cls: type["TrackInstances"], new_meth: ty.Callable[P, object]):
        def __new__(klass: "TrackInstances", *args: P.args, **kwargs: P.kwargs):
            instance = new_meth(klass, *args, **kwargs)  # type: ignore
            klass.instances.add(instance)
            return instance

        return __new__

    def __str__(self) -> str:
        return "<class %s with %r instances>" % (self.__name__, len(self.instances))

    __repr__ = __str__


class TrackMyInstances(metaclass=TrackInstances): ...


class New(ty.Generic[T], TrackMyInstances):
    def __init__(self, new: T) -> None:
        self.new = new

    def __str__(self) -> str:
        return "New(%r)" % self.new

    __repr__ = __str__


class Value(ty.Generic[T], TrackMyInstances):
    def __init__(self, name: str, value: T) -> None:
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return "Value(%r, %r)" % (self.name, self.value)

    __repr__ = __str__


v = New(90)
n = New("Simon")
name = Value("name", "Simon Nganga")
age = Value("age", 21)
school = Value("school", "JKUAT")

print(Value.instances)
print(New.instances)
print(TrackInstances.all_instances)
