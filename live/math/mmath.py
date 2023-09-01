def _gcd(a: int, b: int):
    if b == 0: return a
    return _gcd(b, a % b)

def gcd(a: int, b: int):
    a, b = abs(a), abs(b)
    a, b = (a, b) if a >= b else (a, b)
    return _gcd(a, b)
