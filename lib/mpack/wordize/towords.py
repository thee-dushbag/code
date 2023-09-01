from typing import Any, Iterable
from typing_extensions import Self
from itertools import zip_longest


class groupinto:
    def __init__(self: Self, iterable: Iterable, size: int = 1) -> None:
        size = int(size)
        self.iobj = iter(iterable)
        self.size = size if size > 0 else 1

    def __iter__(self):
        return self

    def __next__(self):
        for group in zip_longest(*[self.iobj for _ in range(self.size)]):
            return group
        raise StopIteration


class NumberSpliter:
    def __init__(self: Self, grpcnt: int = 3, isep: str = "") -> None:
        self.isep = isep
        self.grpcnt = grpcnt

    def split(self, number: int) -> str:
        _var: Any = reversed(str(int(number)))
        _var = list(
            reversed([list(reversed(var)) for var in groupinto(_var, self.grpcnt)])
        )
        _clean = lambda vals: ["0" if val == None else val for val in vals]
        _var = [self.isep.join(_clean(var)) for var in _var]
        return _var


class Symbol:
    def __init__(self, sym: Any, word: str) -> None:
        self.symbol = sym
        self.word = word


class Context:
    def __init__(self) -> None:
        self.symbols: dict[str, Symbol] = dict()
        self.groupcount: dict[int, Symbol] = dict()

    def iszero(self, vals):
        return all([val == self.symbols["0"].word for val in vals])

    def improvise(self: Self, grpcnt: int) -> str:
        assert 1 in self.groupcount, "Cannot function without basic group name."
        return self.groupcount[grpcnt].word

    def verify(self: Self, sval: str) -> tuple[bool, str]:
        for val in sval:
            if val not in self.symbols:
                return False, f"Unknown symbol: {val}"
        return True, ""

    def groupname_fract(self: Self, number: str) -> str:
        if number == "":
            return ""
        return (
            self.symbols["."].word
            + " "
            + " ".join([self.symbols[sym].word for sym in number])
        )

    def groupname_whole(self: Self, grp: str) -> str:
        assert len(grp) == 3, "Group must have 3 integers."
        hundreds = (
            self.symbols[grp[0]].word + f" {self.symbols['100'].word}"
            if grp[0] != "0"
            else ""
        )
        if grp[1] == "1":
            tens = self.symbols[grp[1:]].word
        else:
            n1 = self.symbols[grp[1] + "0"].word if grp[1] != "0" else ""
            n2 = self.symbols[grp[2]].word if grp[2] != "0" else ""
            tens = "" if not (n1 or n2) else n1 + " " + n2
        if hundreds or tens:
            hundreds += (
                f" {self.symbols['cond'].word} " if hundreds and tens else ""
            ) + tens.strip()
        return hundreds if hundreds else self.symbols["0"].word

    def define_symbol(self: Self, sym: Symbol) -> None:
        self.symbols[sym.symbol] = sym

    def define_group(self: Self, sym: Symbol) -> None:
        self.groupcount[sym.symbol] = sym


class Wordizer:
    def __init__(
        self, context: Context, splitter: NumberSpliter, sep: str = ","
    ) -> None:
        self.context = context
        self.splitter = splitter
        self.sep = sep

    def towords(self: Self, number: float, pntz: bool = False) -> str:
        snumber = str(number).split(".")
        if len(snumber) == 1:
            snumber = [*snumber, ""]
        grps = self.splitter.split(int(snumber[0]))
        size = len(grps) - 1
        wholepart = [
            (
                self.context.groupname_whole(grp)
                + f" {self.context.improvise(size - idx)}"
            ).strip()
            for idx, grp in enumerate(grps)
            if self.context.groupname_whole(grp) != self.context.symbols["0"].word
        ]
        if not wholepart:
            wholepart = [self.context.symbols["0"].word]
        if (
            self.context.symbols["cond"].word not in wholepart[-1]
            and size >= 1
            and self.context.symbols["100"].word not in wholepart[-1]
        ):
            wholepart[-1] = f"{self.context.symbols['cond'].word} {wholepart[-1]}"
        fractinalpart = (
            ""
            if snumber[1] == "0" and not pntz
            else self.context.groupname_fract(snumber[1])
        )
        return (", ".join(wholepart) + " " + fractinalpart).strip()
