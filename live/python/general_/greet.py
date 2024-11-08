#!/bin/env python

from sys import stdin, stderr, argv
from os import isatty

class Value:
    def __init__(self, value: str | None = None):
        self.value = value or ""

color = Value("auto")

options = {
    "color": color,
    "c": color
}

for arg in argv[1:]:
    name, _, value = arg.partition("=")
    options.setdefault(name, Value()).value = value

color.value = color.value.lower()

if color.value in ("a", "auto"):
    color.value = "yes" if isatty(1) else "no"

match color.value:
    case "no" | "false" | "n":
        C1 = C2 = C3 = ""
    case "yes" | "true" | "y":
        C1="\033[94m"
        C2="\033[95m"
        C3="\033[0m"
    case other:
        print("Invalid value for color %r: expected oneof (n|no|false|y|yes|true|a|auto)" % other, file=stderr)
        exit(1)

try:
    for name_age in stdin:
        name, _, age = name_age.strip().partition(',')
        print(f"{C1}Hello {C2}{name}{C1}, you are {C2}{age}{C1} years old!{C3}")
except KeyboardInterrupt:
    ...

