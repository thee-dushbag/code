# type: ignore
from .context import Context
from .parse_tree import SymbolTree
from .syntax import LexicalAnalyzer, SyntaxBreaker


class ValueType:
    value: int = 1
    symbol: int = 2


class ValueChecker:
    def __init__(self, values: str) -> None:
        self.values = [ch for ch in values]

    def is_defined(self, val) -> bool:
        for v in val:
            if not v in self.values:
                return False
        return True


class Interpreter:
    def __init__(self, context: Context, values: ValueChecker) -> None:
        self.context = context
        self.values: ValueChecker = values
        self.parse_tree = SymbolTree(context)
        self.syntax_checker = SyntaxBreaker(context, values)
        self.lexical_analyzer = LexicalAnalyzer(context, values)

    def parse(self, mathstr: str) -> float:
        mathstr = self.lexical_analyzer.analyze(mathstr)
        mathstr = self.syntax_checker.analyze(mathstr)
        return self.parse_tree.parse(mathstr).evaluate()
