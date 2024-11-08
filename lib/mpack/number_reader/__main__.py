from sys import argv
from . import get_reader
from os import getenv

locale = getenv("NUMBER_LOCALE")
reader = get_reader(locale or "english")

for number in argv[1:]:
    print(reader(number))

