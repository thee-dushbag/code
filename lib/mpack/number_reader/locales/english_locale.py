from .ilocale import DefaultContext

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

SPECIALS = {".": "point", "conj": "and"}

GROUPS = {
    -1: "hundred",
    0: "",
    1: "thousand",
    2: "million",
    3: "billion",
    4: "trillion",
    5: "quadrillion",
    6: "quintillion",
    7: "sextillion",
    8: "septillion",
    9: "octillion",
    10: "nonillion",
    11: "decillion",
    12: "undecillion",
    13: "duodecillion",
    14: "tredecillion",
    15: "quattuordecillion",
    16: "quindecillion",
    17: "sexdecillion",
    18: "septendecillion",
    19: "octodecillion",
    20: "novemdecillion",
    21: "vigintillion",
}

context = DefaultContext({**TENS, **BASIC_NUMBERS, **TENS_UNIQUE}, GROUPS)
context.addspecial(**SPECIALS)
