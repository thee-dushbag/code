# type: ignore
from typing import Callable, Protocol

from math_interpreter.context import Context, SymbolType
from math_interpreter.parse_tree import StringLike


class ValueType(Protocol):
    value: int = 1
    symbol: int = 2


class ValueChecker(Protocol):
    def __init__(self, values: str) -> None:
        pass

    def is_defined(self, val) -> bool:
        pass


class LexicalAnalyzer:
    def __init__(self, symbols: Context, values: ValueChecker) -> None:
        self.sym_checker: Context = symbols
        self.val_checker: ValueChecker = values

    def analyze(self, mathstr: str) -> str:
        self.check_all_symbols(mathstr)
        return mathstr

    def check_all_symbols(self, mathstr: str):
        check: Callable[[str], bool] = lambda ch: self.sym_checker.is_defined(
            ch
        ) or self.val_checker.is_defined(ch)
        for i, ch in enumerate(mathstr):
            if ch == " ":
                continue
            assert check(ch), f"Unknown symbol: {ch} at index {i} in {mathstr}"


class OpCrusher:
    def __init__(self, context: Context, template: str) -> None:
        self.context: Context = context
        self.template = template

    def resolve_dblsym(self, tokens) -> None:
        targets = []
        prev = None
        for index, token in enumerate(tokens):
            cur = self.context.is_defined(token)
            if cur == prev == True:
                targets.append(index)
            prev = cur
        while targets:
            cur = targets.pop(0)
            rside = tokens[cur + 1]
            tokens[cur] = self.template.format(lside="", rside=rside, symb=tokens[cur])

    def crush(self, tokens: list[str], symb: str) -> str:
        self.resolve_dblsym(tokens)
        while symb in tokens:
            tokens = self._crush(tokens, symb)
        return tokens

    def _crush(self, tokens: str, symb: str) -> str:
        cache: list[str] = []
        for index, val in enumerate(tokens):
            if val != symb:
                cache.append(val)
            else:
                break
        lside = None
        if cache:
            lside = cache[-1]
        rside = tokens[index + 1]
        if self.context.is_defined(lside):
            lside = None
        else:
            if cache:
                cache.pop()
        temp = self.template.format(
            lside=lside if lside else "", symb=symb, rside=rside
        )
        cache.append(temp)
        if (index + 2) < len(tokens):
            cache.extend(tokens[index + 2 :])
        return cache

    def _update(self, tokens: list[str], val: str) -> None:
        if self.context.is_defined(val):
            tokens.append(val)
            tokens.append("")
        else:
            if tokens:
                tokens[-1] += val
            else:
                tokens.append(val)

    def breaker(self, string: str) -> list[str]:
        string: StringLike = StringLike(string)
        tokens: list[str] = []
        while string.string:
            ch = string.pop(0)
            if ch == " ":
                continue
            self._update(tokens, ch)
        return [tok for tok in tokens if tok != ""]


class SyntaxBreaker:
    def __init__(self, symbols: Context, values: ValueChecker) -> None:
        self.context: Context = symbols
        self.values: ValueChecker = values
        self.opcrusher: OpCrusher = OpCrusher(symbols, "{symb}({lside},{rside})")

    def analyze(self, mathstr: str) -> str:
        tokens = self.opcrusher.breaker(mathstr)
        self.verify_sym_types(tokens)
        symbs = [sym for sym in tokens if self.check_type(sym) == ValueType.symbol]
        prefs = {self.context.get_pref(sym): sym for sym in symbs}
        prefs_sort = sorted([key for key in prefs])
        while prefs_sort:
            key = prefs_sort.pop()
            sym = prefs[key]
            tokens = self.opcrusher.crush(tokens, sym)
        return f"+({tokens[0]},0)" if tokens[0].isdigit() else tokens[0]

    def check_type(self, ch) -> ValueType:
        if self.context.is_defined(ch):
            return ValueType.symbol
        elif self.values.is_defined(ch):
            return ValueType.value
        raise RuntimeError(f"Symbol error: Symbol not defined '{ch}'")

    def verify_sym_sig(self, sym, lside, rside):
        sig = SymbolType.binary if rside and lside else None
        if rside and not lside:
            sig = SymbolType.unary
        symtype = self.context.get_sym_type(sym)
        res = self.context.cmp_sym_type(sig, symtype)
        return res

    def verify_sym_types(self, tokens: list[str]):
        symbs = [
            [index, symb]
            for index, symb in enumerate(tokens)
            if self.check_type(symb) == ValueType.symbol
        ]
        for index, symb in symbs:
            if len(tokens) > (index + 1):
                rside = tokens[index + 1]
            else:
                rside = ""
            if index == 0:
                lside = ""
            else:
                lside = tokens[index - 1]
            if self.check_type(lside) == ValueType.symbol:
                assert self.verify_sym_sig(
                    symb, None, rside
                ), f"Symbol misuse: {symb} is not unary as used.\n\t{lside} {symb} {rside}"
                continue
            assert self.verify_sym_sig(
                symb, lside, rside
            ), f"Symbol misuse: {symb} is not binary as used.\n\t{lside} {symb} {rside}"
