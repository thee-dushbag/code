BASIC_NUMBERS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}

TENS_UNIQUE = {
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
}

TENS = {
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
}

GROUPS = {0: "", 1: "thousand", 2: "million", 3: "billion", 4: "quadtillion"}

SPECIALS = {".": "point", "cond": "and", "100": "hundred"}

from .towords import (
    Context,
    Symbol,
    Wordizer,
    NumberSpliter,
)
from itertools import chain

_context = Context()

for sym, name in chain(
    BASIC_NUMBERS.items(), TENS_UNIQUE.items(), TENS.items(), SPECIALS.items()
):
    _context.define_symbol(Symbol(str(sym), name))

for sym, name in GROUPS.items():
    _context.define_group(Symbol(sym, name))

_splitter = NumberSpliter()
towords = Wordizer(_context, _splitter).towords
