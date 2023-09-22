from .context import Context, SymbolType
from .definitions import Interpreter, ValueChecker
from .symbols import (CombSymbol, DivSymbol, FactSymbol, FloorSymbol,
                      ModSymbol, MulSymbol, PermSymbol, PowSymbol, RatiSymbol,
                      SubSymbol, SumSymbol)

# *    3 * 9 + 5 / 7
# *    +(3*9,5/7)
# *    +(*(3,9),/(5,7))

# *             +   SumSymbol
# *             |
# *        -----------
# *       |           |
# *       *           /    MulSymbol, DivSymbol
# *       |           |
# *    -------     -------
# *   |       |   |       |
# *   3       9   5       7 ValueSymbol

_context: Context = Context()
_context.add_symbol("+", 1006, SumSymbol, SymbolType.bnu)
_context.add_symbol("-", 1007, SubSymbol, SymbolType.bnu)
_context.add_symbol("*", 1008, MulSymbol, SymbolType.binary)
_context.add_symbol("%", 1009, ModSymbol, SymbolType.binary)
_context.add_symbol("/", 1010, DivSymbol, SymbolType.binary)
_context.add_symbol("&", 1011, FloorSymbol, SymbolType.binary)
_context.add_symbol("^", 1012, PowSymbol, SymbolType.binary)
_context.add_symbol("!", 1013, FactSymbol, SymbolType.unary)
_context.add_symbol("P", 1014, PermSymbol, SymbolType.binary)
_context.add_symbol("C", 1015, CombSymbol, SymbolType.binary)
_context.add_symbol("o", 1016, RatiSymbol, SymbolType.binary)

_numric_checker: ValueChecker = ValueChecker("0123456789.")
parser: Interpreter = Interpreter(_context, _numric_checker)
