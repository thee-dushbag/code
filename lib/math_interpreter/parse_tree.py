#type: ignore
from typing import Any
from .context import Context
from .symbols import Value

class StringLike:
    def __init__(self, string: str = '') -> None:
        self.string: list[str] = [char for char in string]
    
    def pop(self, index: int = -1) -> str:
        return self.string.pop(index) if self.string else ''
    
    def push(self, char: str) -> None:
        self.string.append(char)
    
    def at(self, index: int = 0) -> str:
        return self.string[index]
    
    def join(self, dlm: str = '') -> str:
        return dlm.join(self.string)


class SymbolTree:
    def __init__(self, context: Context) -> None:
        self.context: Context = context

    def parse(self, tree_text: str) -> Any:
        if not tree_text: return None
        string: StringLike = StringLike(tree_text)
        symbname = StringLike()
        while string.at(0) != '(':
            symbname.push(string.pop(0))
        string.pop(0)
        string.pop()
        left, right = self.expr_seperator(string.join())
        nleft: Value | SymbolTree = Value(left) if left.isdigit() else self.parse(left)
        nright: Value | SymbolTree = Value(right) if right.isdigit() else self.parse(right)
        sname: str = symbname.join()
        symbol = self.context.get_symb(sname)
        return symbol(sname, nleft, nright if nright else None)


    def expr_seperator(self, text: str) -> list[str]:
        inscope:list[int] = []
        index: int = 0
        for i, char in enumerate(text):
            if char == '(':
                inscope.append(True)
            elif char == ')':
                inscope.pop()
            elif char == ',' and not inscope:
                index = i
                break
        return [text[:index], text[index + 1:]]