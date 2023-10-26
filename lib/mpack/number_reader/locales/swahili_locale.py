from .ilocale import DefaultContext, IContext, ILocale

BASIC_NUMBERS = {
    0: "sufuri",
    1: "moja",
    2: "mbili",
    3: "tatu",
    4: "nne",
    5: "tano",
    6: "sita",
    7: "saba",
    8: "nane",
    9: "tisa",
}

COMB = {
    10: "kumi",
    20: "ishirini",
    30: "thelathini",
    40: "arobaini",
    50: "hamsini",
    60: "sitini",
    70: "sabini",
    80: "themanini",
    90: "tisini",
}

GROUPS = {-1: "mia", 0: "", 1: "elfu", 2: "milioni", 3: "bilioni", 4: "trilioni"}

SPECIALS = {".": "pointi", "conj": "na"}

context = DefaultContext({**COMB, **BASIC_NUMBERS}, GROUPS)
context.addspecial(**SPECIALS)
