from .english_locale import context as english_context
from .swahili_locale import context as swahili_context
from .french_locale import context as french_context
from .ilocale import DefaultLocale, side
import enum

english_locale = DefaultLocale(english_context, side.right, side.right, False, True)
french_locale = DefaultLocale(french_context, side.right, side.right, True, True)
swahili_locale = DefaultLocale(swahili_context, side.left, side.left, True, True)

class Locale(enum.StrEnum):
    SWAHILI = enum.auto()
    ENGLISH = enum.auto()
    FRENCH = enum.auto()

locales = {
    Locale.ENGLISH: english_locale,
    Locale.SWAHILI: swahili_locale,
    Locale.FRENCH: french_locale
}