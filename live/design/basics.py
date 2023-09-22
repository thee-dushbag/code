class A:
    pass


class B(A):
    pass


class C(B):
    pass


def covariant_example(items: B) -> None:
    print(items.__class__.__name__)


def contravariant_example(item: A) -> None:
    print(item.__class__.__name__)


# Valid Covariance Example
b_item: B = B()
covariant_example(b_item)  # Output: "B"

# Valid Contravariance Example
a_item: A = A()
contravariant_example(a_item)  # Output: "A"

# Invalid Covariance Example (should raise a type error)
c_item: C = C()
covariant_example(c_item)  # Raises TypeError since covariant_example expects B

# Invalid Contravariance Example (should raise a type error)
contravariant_example(c_item)  # Raises TypeError since contravariant_example expects A
