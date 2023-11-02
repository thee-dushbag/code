from .locales.ilocale import ILocale
from .utils import NumberSpliter


class NumberReader:
    def __init__(self, locale: ILocale) -> None:
        self.locale = locale
        self.ns = NumberSpliter()

    def read(self, number: float, ignore_pz: bool = True) -> str:
        snum = f'{number:f}'.split(".")
        assert float(number), f"Expected a number, got {number}"
        if len(snum) == 1:
            snum.append("0")
        elif not int(snum[1]):
            snum[1] = '0'
        wnum, dnum = snum
        groups = self.ns.split(wnum)
        grpnames = [
            self.locale.read_tridigit_number(group) if int(group) else ""
            for group in groups
        ]
        grpnames = reversed(grpnames)
        namedgroups = [
            self.locale.group(group, index) if group else ""
            for index, group in enumerate(grpnames)
        ]
        namedgroups = list(reversed(namedgroups))
        dname = (
            "" if dnum == "0" and ignore_pz else self.locale.read_decimal_number(dnum)
        )
        return " ".join((self.locale.join(namedgroups), dname)).strip()
