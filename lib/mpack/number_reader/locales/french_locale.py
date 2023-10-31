from .ilocale import DefaultContext

BASIC_NUMBERS = {
    0: "zero",
    1: "un",
    2: "deux",
    3: "trois",
    4: "quatre",
    5: "cinq",
    6: "six",
    7: "sept",
    8: "huit",
    9: "neuf",
}

TENS_UNIQUE = {
    11: "onze",
    12: "donze",
    13: "treize",
    14: "quatorze",
    15: "quinze",
    16: "seize",
}

TENS = {
    10: "dix",
    20: "vingt",
    30: "trente",
    40: "quarante",
    50: "cinquante",
    60: "soixante",
    70: "septante",
    80: "huitante",
    90: "nonante",
}

SPECIALS = {"conj": "et", "tens_conj": "-", ".": "virgule"}

GROUPS = {
    -1: "cent",
    0: "",
    1: "mille",
    2: "million",
    3: "milliard",
    4: "mille milliards",
    5: "quadrillion",
    6: "quintillion",
    7: "sextillion",
    8: "septillion",
    9: "octillion",
    10: "nonillion",
    11: "décillion",
    12: "undécillion",
    13: "duodécillion",
    14: "tredécillion",
    15: "quatre décillions",
    16: "quindécillion",
    17: "sexedécillion",
    18: "septendécillion",
    19: "octodécillion",
    20: "novembredécillion",
    21: "vingt milliards",
}

context = DefaultContext(
    numbers={**BASIC_NUMBERS, **TENS_UNIQUE, **TENS}, grpmaps=GROUPS
)
context.addspecial(**SPECIALS)
