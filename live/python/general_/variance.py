"""
COVARIANCE AND CONTRAVARIANCE
=============================
Covariance
----------
  Applies to parameters where you are
  allowed to pass the type and its
  subclasses as the value of the parameter.
  Example:
    In the covariant_fn function below,
    any instance of B and C are valid but
    type A is not. This is because, A is
    (thinner)lacks some properties of B
    while C has all and additional ones that
    might not be needed.
    All instances of B have methods a() and b()
    while C has an additional method c()
    therefore all instances of C are also B. As
    for A it lacks method b(), hence not a B.
  In short, covariance is positive, that is,
  for a class B, a parameter of type B can
  be assigned an instance of type B or any
  subclass of B since they are valid B's.

Contravariance
--------------
  Applies to return types of a function. A
  variable that tries to hold the value returned
  has to be of the same type as the return type
  or a base class of the return type.
  Example:
    In the contravariant_fn function below,
    any variable of type or its subclass can be
    assigned the value returned since all B's
    are also A's. Variable of type C cannot hold
    the value since it requires some properties
    that are not present in B, that is c(). All
    B's have b() and a() and all A's have a(),
    with this, any B, is also an A.
"""

from functools import wraps
from typing import TypeVar

# Used in place of covariant Types
T = TypeVar("T", covariant=True)
# Used in place of contravariant Types
U = TypeVar("U", contravariant=True)


class A:
    def a(self):
        print("A.a()")


class B(A):
    def b(self):
        print("B.b()")


class C(B):
    def c(self):
        print("C.c()")


def contravariant_fn() -> B:
    return B()


def covariant_fn(_: B) -> None:
    ...


# A() is narrower than B
# hence it cannot be passed
# in place of B. It lacks b().
covariant_fn(A())

# Okay since passed type
# and parameter type are equal.
covariant_fn(B())

# Okay since all C's are also B's.
covariant_fn(C())

# Okay since all B's are also A's.
a: A = contravariant_fn()

# Okay since return type
# and varible type are equal.
b: B = contravariant_fn()

# C cannot hold a B, since it
# is wider than B. All C's are
# thicker B's, that is, C has
# properties B lacks, like c().
c: C = contravariant_fn()


# Examples:
def attr_error(func):
    @wraps(func)
    def attr(value):
        try:
            return func(value)
        except AttributeError as e:
            print(str(e))

    return attr


@attr_error
def call_a(a: A) -> None:
    print(
        f"[expect: A in call_a] Calling: a.a() | type(a) = {type(a).__name__}",
        end=" : ",
    )
    a.a()


@attr_error
def call_b(b: B) -> None:
    print(
        f"[expect: B in call_b] Calling: b.b() | type(a) = {type(b).__name__}",
        end=" : ",
    )
    b.b()


@attr_error
def call_c(c: C) -> None:
    print(
        f"[expect: C in call_c] Calling: c.c() | type(a) = {type(c).__name__}",
        end=" : ",
    )
    c.c()


def make_a() -> A:
    return A()


def make_b() -> B:
    return B()


def make_c() -> C:
    return C()


# Covariance Examples.
_a: A = A()
call_a(_a)  # Okay
call_b(_a)  # A lacks B.b()
call_c(_a)  # A lacks C.c()
print()

_b: B = B()
call_a(_b)  # Okay
call_b(_b)  # Okay
call_c(_b)  # B lacks C.c()
print()

_c: C = C()
call_a(_c)  # Okay
call_b(_c)  # Okay
call_c(_c)  # Okay

del _a, _b, _c

# Contravariant Examples.
_a: A = make_a()  # Okay
_b: B = make_a()  # A lacks B.b()
_c: C = make_a()  # A lacks C.c()

_a: A = make_b()  # Okay
_b: B = make_b()  # Okay
_c: C = make_b()  # B lacks C.c()

_a: A = make_c()  # Okay
_b: B = make_c()  # Okay
_c: C = make_c()  # Okay
del _a, _b, _c
