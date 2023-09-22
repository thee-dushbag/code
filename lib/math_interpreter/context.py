# type: ignore
from enum import Enum
from typing import Any

from .symbols import Symbol


class SymbolType(Enum):
    unary: int = 1
    binary: int = 2
    bnu: int = 3


class SymbolRep:
    def __init__(self, symb: str, pref: int, symobj: Symbol, stype: SymbolType) -> None:
        self.type = stype
        self.symbol: str = symb
        self.pref: int = pref
        self.symobj: Symbol = symobj


class Context:
    def __init__(self) -> None:
        self.context: dict[str, SymbolRep] = {}

    def add_symbol(self, symb: str, pref: int, symobj: Any, stype: SymbolType) -> None:
        self.context[symb] = SymbolRep(symb, pref, symobj, stype)

    def is_defined(self, symb: str) -> bool:
        return symb in self.context.keys()

    def get_pref(self, symb: str) -> int:
        return self.context[symb].pref

    def get_symb(self, symb: str) -> Any:
        return self.context[symb].symobj

    def get_sym_type(self, symb) -> int:
        return self.context[symb].type

    def cmp_sym_type(self, sym, expt) -> bool:
        expt = (
            [SymbolType.unary, SymbolType.binary, SymbolType.bnu]
            if expt == SymbolType.bnu
            else [expt]
        )
        # print(f"Checking for {cur} in {expt}")
        return sym in expt
