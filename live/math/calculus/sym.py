import sympy as sy

x, y, z = sy.symbols("x,y,z")


def arc_length(func: sy.Expr):
    deriv: sy.Expr = 1 + func.diff() ** 2
    deriv = sy.sqrt(deriv)
    return deriv.integrate()


def subrange(func: sy.Expr, x: sy.Symbol, a: float, b: float):
    return func.subs(x, b) - func.subs(x, a)  # type:ignore


def fsubrange(func: sy.Expr, x: sy.Symbol, a: float, b: float):
    return float(subrange(func, x, a, b))


def surface_area(func: sy.Expr):
    integral = func * arc_length(func)
    integral = 2 * sy.pi * integral.integrate()
    return integral


def volume(func: sy.Expr):
    return sy.pi * (func**2).integrate()
