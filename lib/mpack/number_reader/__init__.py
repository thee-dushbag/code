from typing import Callable, Optional
from .locales import locales, Locale
from .reader import NumberReader

Reader = Callable[[float], str]
ReaderB = Callable[[float, Optional[bool]], str]

def get_reader(locale: Locale | str) -> Reader:
    if not isinstance(locale, Locale):
        locale = Locale(str(locale).lower())
    _locale = locales[locale]
    reader = NumberReader(_locale)
    return reader.read
