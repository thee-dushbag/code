import typing as ty, operator as op


def _resolve(a, b, c):
    if b is None and c is None:
        a, b, c = 0, a, 1
    elif c is None:
        c = 1
    assert all(map(lambda v: isinstance(v, int), (a, c, b)))
    return a, b, c


@ty.overload
def count(stop: int, /) -> ty.Generator[int, None, None]:
    ...


@ty.overload
def count(start: int, stop: int, /) -> ty.Generator[int, None, None]:
    ...


@ty.overload
def count(start: int, stop: int, step: int, /) -> ty.Generator[int, None, None]:
    ...


def _count_impl(st, sp, s):
    cmp = op.lt if s > 0 else op.gt
    while cmp(st, sp):
        yield st
        st += s


def count(start, stop=None, step=None, /):
    values = _resolve(start, stop, step)
    assert all(map(lambda v: isinstance(v, int), values))
    return _count_impl(*values)


from more_itertools import polynomial_derivative as diff
from itertools import tee


def line_equation(point, gradient):
    return [gradient, -point[0] * gradient + point[1]]


def polynomial_equation(coefficients):
    n = len(coefficients)
    powers = reversed(range(n))
    power = lambda p: f"x^{p}" if p > 1 else "x" * p
    merge = lambda c, p: f"{c}{power(p)}"
    return " + ".join(map(merge, coefficients, powers))


def polynomial_eval(coefficients, x):
    n = len(coefficients)
    powers = reversed(range(n))
    return sum(map(lambda c, p: c * x**p, coefficients, powers))


def polynomial_integral(coefficients, C=0):
    n = len(coefficients)
    powers = reversed(range(n))
    icoef = lambda c, p: c / (p + 1)
    coeffs = list(map(icoef, coefficients, powers))
    coeffs.append(C)
    return coeffs


def test_eqs():
    eval = polynomial_eval
    equa = polynomial_equation
    integ = polynomial_integral

    x = 10
    coef = [3, 5, 2]
    dcoef = diff(coef)
    icoef = integ(coef)
    func = f"y(x) = {equa(coef)}"
    deriv = f"y`(x) = {equa(dcoef)}"
    integral = f"Y(x) = {equa(icoef)}"

    L = line_equation([x, eval(coef, x)], eval(dcoef, x))
    print(func)
    print(deriv)
    print(integral)
    print(f"Area(3, 10) = Y(10) - Y(3) =", eval(icoef, 10) - eval(icoef, 3))
    print(f"y({x}) =", eval(coef, x))
    print(f"y`({x}) =", eval(dcoef, x))
    print("L(x) =", equa(L))

    I = integ(dcoef, 2)
    print(equa(I), I == coef)


# print(list(count(10)))
# print(list(count(5, 10)))
# print(list(count(5, 10, 2)))


def _perm_impl(n: int, r: int) -> int:
    p = 1
    for v in range(n + 1 - r, n + 1):
        p *= v
    return p


def _comb_impl(n: int, r: int) -> int:
    k, c = min(r, n - r), 1
    for r in range(1, k + 1):
        c *= (n - k + r) // r
    return c


def _assert_nr(n, r):
    assert all(
        map(isinstance, (n, r), (int, int))
    ), "Expected n and r to be integers, got type(n)=%r, type(r)=%r" % map(type, (n, r))

    assert (
        r <= n and n >= 0 and r >= 0
    ), "Requires: n >= r, n >= 0, r >= 0. got: n=%r, r=%r." % (n, r)


def perm(n: int, r: int | None = None, /) -> int:
    r = n if r is None else r
    _assert_nr(n, r)
    return _perm_impl(n, r)


def comb(n: int, r: int | None = None, /) -> int:
    r = n if r is None else r
    _assert_nr(n, r)
    return _comb_impl(n, r)


def test_iters():
    values = list(range(1, 11))
    i1 = iter(values)
    i2 = iter(values)
    assert i1 is not i2
    c1 = iter(values)
    c2, c3 = tee(c1)
    print(*map(list, (c2, c3)))


from mpack.timer import timer_sync
from math import factorial


def fperm(n: int, r: int):
    num = factorial(n)
    den = factorial(n - r)
    return num // den


def fcomb(n: int, r: int):
    perm = fperm(n, r)
    den = factorial(r)
    return perm // den


@timer_sync
def factorial_permcomb(n: int, r: int):
    fperm(n, r)
    fcomb(n, r)


@timer_sync
def linear_permcomb(n: int, r: int):
    _perm_impl(n, r)
    _comb_impl(n, r)


def speed_test():
    from sys import set_int_max_str_digits

    n, r = 1_000_000, 1_000
    set_int_max_str_digits(n)

    print(linear_permcomb(n, r))
    print(factorial_permcomb(n, r))
