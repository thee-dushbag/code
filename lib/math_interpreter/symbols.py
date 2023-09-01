#type: ignore
from abc import ABC, abstractmethod

class Symbol:
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        self.symbol: str = symbol
        self.right: Symbol = rnode
        self.left: Symbol = lnode

    @abstractmethod
    def evaluate(self) -> float:
        pass

    def __str__(self) -> str:
        return f'Symbol({self.symbol}, {self.left}, {self.right})'

class Value(Symbol):
    def __init__(self, value: str) -> None:
        super().__init__(value, None, None)

    def evaluate(self) -> float:
        return float(self.symbol)

    def __str__(self) -> str:
        return f'Value({self.symbol})'

class SumSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol' = None) -> None:
        super().__init__(symbol, lnode, rnode)

    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate() if self.left else 0
        right: float | Literal[0] = self.right.evaluate() if self.right else 0
        return left + right

class SubSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol' = None) -> None:
        super().__init__(symbol, lnode, rnode)

    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate() if self.left else 0
        right: float | Literal[0] = self.right.evaluate() if self.right else 0
        return left - right

class MulSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)

    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        return left * right

class DivSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)

    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        if right == 0: raise ZeroDivisionError(f"Trying to divide by zero: {left}/{right}")
        return left / right

class PowSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)

    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        return pow(left, right)
    
class ModSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)
    
    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        if right == 0: raise ZeroDivisionError(f"Trying to divide by zero: {left}%{right}")
        return left % right

class FloorSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)
    
    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        if right == 0: raise ZeroDivisionError(f"Trying to divide by zero: {left}//{right}")
        return left // right
    
class FactSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)
    
    @staticmethod
    def factorial(n) -> int:
        return 1 if n == 0 else n * FactSymbol.factorial(n - 1)

    def evaluate(self) -> float:
        left: float | Literal[0] = self.right.evaluate()
        assert left >= 0, "Cannot compute value for negative factorials."
        return self.factorial(int(left))

class CombSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)
    
    @staticmethod
    def combination(n, r) -> int:
        num = FactSymbol.factorial(n)
        den = FactSymbol.factorial(n - r) * FactSymbol.factorial(r)
        return num/den

    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        return CombSymbol.combination(left, right)

class PermSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)
    
    @staticmethod
    def permutation(n, r) -> int:
        num = FactSymbol.factorial(n)
        den = FactSymbol.factorial(n - r)
        return num/den

    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        return PermSymbol.permutation(left, right)
    
class RatiSymbol(Symbol):
    def __init__(self, symbol: str, lnode: 'Symbol', rnode: 'Symbol') -> None:
        super().__init__(symbol, lnode, rnode)
    
    def evaluate(self) -> float:
        left: float | Literal[0] = self.left.evaluate()
        right: float | Literal[0] = self.right.evaluate()
        return left / right