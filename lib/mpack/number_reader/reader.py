from .locales.ilocale import ILocale
from .utils import NumberSpliter


class NumberReader:
    def __init__(self, locale: ILocale) -> None:
        self.locale = locale
        self.ns = NumberSpliter()

    def read(self, number: float, ignore_pz: bool = True) -> str:
        snum = str(number).split(".")
        wnum = snum[0]
        if len(snum) == 2:
            dnum = snum[1]
        else:
            dnum = "0"
        groups = self.ns.split(int(wnum))
        grpnames = [self.locale.read_tridigit_number(group) for group in groups]
        grpnames = reversed(grpnames)
        namedgroups = [
            self.locale.group(group, index) for index, group in enumerate(grpnames)
        ]
        namedgroups = list(reversed(namedgroups))
        dname = (
            "" if dnum == "0" and ignore_pz else self.locale.read_decimal_number(dnum)
        )
        return " ".join((self.locale.join(namedgroups), dname)).strip()
