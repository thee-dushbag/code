from enum import Enum
from typing import Annotated, Protocol


class ILocale(Protocol):
    def group(self, grp_name: str, grp_index: int) -> str:
        ...

    def read_tridigit_number(self, number: str) -> str:
        ...

    def read_decimal_number(self, number: str) -> str:
        ...

    def join(self, names: list[str]) -> str:
        ...

    def __init__(self, context: "IContext") -> None:
        ...


class IContext(Protocol):
    def getspecial(self, key: str) -> str | None:
        ...

    def addspecial(self, **maps) -> str | None:
        ...

    def gettens(self, number: str) -> str | None:
        ...

    def getones(self, number: str) -> str | None:
        ...

    def gethuns(self, number: str) -> str | None:
        ...

    def addnumb(self, number: Annotated[str, "A number with atmost 3 digits."]):
        ...

    def getgrp(self, grpcnt: str | int) -> str | None:
        ...

    def addgrp(self, grpcnt: int, grpname: str) -> None:
        ...

class DefaultContext(IContext):
    def __init__(
        self,
        numbers: dict[int | str, str] | None = None,
        grpmaps: dict[int | str, str] | None = None,
    ) -> None:
        self.ones = {}
        self.tens = {}
        self.huns = {}
        self.groups = {}
        self.special = {}
        if numbers:
            self.addnumb(**{str(int(key)): value for key, value in numbers.items()})
        if grpmaps:
            self.addgrp(**{str(key): val for key, val in grpmaps.items()})

    def addspecial(self, **special_maps) -> None:
        self.special = {**self.special, **special_maps}

    def getspecial(self, key: str) -> str | None:
        return self.special.get(key, None)

    def _special(self, number: str) -> str | None:
        return self.getones("0") if ("0" * len(number)) == number else None

    def getones(self, number: str) -> str | None:
        return self.ones.get(number, None) or self._special(number)

    def gettens(self, number: str) -> str | None:
        return self.tens.get(number, None) or self._special(number)

    def gethuns(self, number: str) -> str | None:
        return self.huns.get(number, None) or self._special(number)

    def getgrp(self, grpcnt: str | int) -> str | None:
        return self.groups.get(int(grpcnt), None)

    def addgrp(self, **groups: str) -> None:
        self.groups = {
            **self.groups,
            **{int(key): value for key, value in groups.items()},
        }

    def addnumb(self, **numbers: str) -> None:
        for number, name in numbers.items():
            key = str(number).lstrip("0") or "0"
            assert key.isnumeric(), f"Number passed: '{key}' is not a digit."
            assert (
                1 <= len(key) <= 3
            ), f"Number passed: '{key}' does not contain atmost 3 digits or atleast 1 digit."
            (self.ones, self.tens, self.huns)[len(key) - 1][key] = name


class side(Enum):
    left = 0
    right = 1


class DefaultLocale(ILocale):
    def __init__(self, context: IContext, hside: side, gside: side, tconj: bool = False, sconj: bool = True, sep:str = ', ') -> None:
        self.context = context
        self.group_name_side: side = gside
        self.hundred_name_side: side = hside
        self.tens_has_conj = tconj
        self.surround_conj_space = sconj
        self.space = ' ' if self.surround_conj_space else ''
        self.sep = sep

    def read_decimal_number(self, number: str) -> str:
        assert number.isnumeric(), "Decimal part must be numeric."
        point = self.context.getspecial(".") or "point"
        numbers = (str(self.context.getones(num)) for num in number)
        return f"{point} {' '.join(numbers)}"

    def group(self, grp_name: str, grp_index: int) -> str:
        group_name = self.context.getgrp(grp_index)
        if grp_name == self.context.getones('0'): return grp_name
        return (
            f"{group_name} {grp_name}"
            if self.group_name_side == side.left
            else f"{grp_name} {group_name}"
        ).strip()

    def read_tridigit_number(self, number: str) -> str:
        assert (
            len(number) == 3 and number.isnumeric()
        ), f"Number '{number}' is not a 3-digit number."
        if hunds := self.context.gethuns(number):
            return hunds
        hunds = "" if number[0] == "0" else self.context.getones(number[0])
        if hunds:
            hund_name = self.context.getgrp(-1)
            hunds = (
                f"{hund_name} {hunds}"
                if self.hundred_name_side == side.left
                else f"{hunds} {hund_name}"
            )
        tens = self._read_bidigit_number(number[1:])
        tens = "" if self.context.getones("0") == tens else tens
        conj = self.context.getspecial("conj")
        if (f"{self.space}{conj}{self.space}" not in tens) and hunds and tens:
            tens = f"{conj}{self.space}{tens}"
        return " ".join((hunds, tens)).strip()  # type: ignore

    def _read_bidigit_number(self, number: str) -> str:  # type: ignore
        if tens := self.context.gettens(number):
            return tens
        one = self.context.getones(number[1])
        tens = "" if number[0] == "0" else self.context.gettens(number[0] + "0")
        ones = "" if number[1] == "0" else one
        conj = self.context.getspecial('tens_conj') or f"{self.space}{self.context.getspecial('conj')}{self.space}" if self.tens_has_conj else self.space
        if ones and tens:
            return f'{tens}{conj}{ones}'.strip()
        elif ones and not tens:
            return str(ones).strip()
        elif tens and not ones:
            return one.strip()  # type: ignore

    def join(self, names: list[str]) -> str:
        if not names:
            raise ValueError("List of group names is empty.")
        if len(names) == 1:
            return names[0]
        conj = str(self.context.getspecial("conj"))
        names = [name for name in names if name]
        if len(names) >= 2 and f"{self.space}{conj}{self.space}" not in names[-1]:
            names[-1] = f'{names[-2]}{self.space}{conj}{self.space}{names[-1]}'
            names.pop(-2)
        return self.sep.join(names)
