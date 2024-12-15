import typing

type SymbolTable = dict[str, bool]


class Base:
    def __repr__(self) -> str:
        return str(self)

    def visit[T](self, visitor: "Visitor[T]") -> T:
        raise NotImplementedError(visitor)

    def __and__(self, other: "Base") -> "Base":
        return And(self, other)

    def __or__(self, other: "Base") -> "Base":
        return Or(self, other)

    def __rand__(self, other: "Base") -> "Base":
        return And(other, self)

    def __ror__(self, other: "Base") -> "Base":
        return Or(other, self)

    def __neg__(self) -> "Base":
        return Not(self)


class And(Base):
    def __init__(self, left: Base, right: Base):
        self.left = left
        self.right = right

    def visit[T](self, visitor: "Visitor[T]") -> T:
        return visitor.visit_and(self)

    def __str__(self) -> str:
        return f"({self.left} & {self.right})"


class Or(Base):
    def __init__(self, left: Base, right: Base):
        self.left = left
        self.right = right

    def visit[T](self, visitor: "Visitor[T]") -> T:
        return visitor.visit_or(self)

    def __str__(self) -> str:
        return f"({self.left} | {self.right})"


class Not(Base):
    def __init__(self, operand: Base):
        self.operand = operand

    def visit[T](self, visitor: "Visitor[T]") -> T:
        return visitor.visit_not(self)

    def __str__(self) -> str:
        return f"!{self.operand}"


class Symbol(Base):
    def __init__(self, name: str):
        self.name = name

    def visit[T](self, visitor: "Visitor[T]"):
        return visitor.visit_symbol(self)

    def __str__(self) -> str:
        return self.name


class Visitor[T](typing.Protocol):
    def visit_and(self, node: And) -> T: ...
    def visit_or(self, node: Or) -> T: ...
    def visit_symbol(self, node: Symbol) -> T: ...
    def visit_not(self, node: Not) -> T: ...


class Exceutor(Visitor[bool]):
    def __init__(self, context: SymbolTable | None = None):
        self.context = context or {}

    def visit_symbol(self, node: Symbol) -> bool:
        return self.context[node.name]

    def visit_or(self, node: Or) -> bool:
        return node.left.visit(self) or node.right.visit(self)

    def visit_and(self, node: And) -> bool:
        return node.left.visit(self) and node.right.visit(self)

    def visit_not(self, node: Not) -> bool:
        return not node.operand.visit(self)

    def execute(self, expr: Base) -> bool:
        return expr.visit(self)


class OptNand(Visitor[Base]):
    def visit_symbol(self, node: Symbol) -> Base:
        return node

    def visit_and(self, node: And) -> Base:
        left = node.left.visit(self)
        right = node.right.visit(self)
        return Not(Not(And(left, right)))

    def visit_or(self, node: Or) -> Base:
        left = Not(node.left).visit(self)
        right = Not(node.right).visit(self)
        return Not(And(left, right))

    def visit_not(self, node: Not) -> Base:
        match node.operand:
            case And() | Not(operand=And()):
                return node
            case Not(operand=Not(operand=operand)):
                return operand.visit(self)
        return Not(node.operand.visit(self))

    def optimize(self, node: Base) -> Base:
        return node.visit(self)


def main():
    a, b = map(Symbol, "ab")
    xor = -((a & b) | (-a & -b))
    print(f"{xor = }")
    opt = OptNand()
    xor = opt.optimize(xor)
    print(f"{xor = }")
    exec = Exceutor()
    for A in [True, False]:
        exec.context["a"] = A
        for B in [True, False]:
            exec.context["b"] = B
            print(exec.context, exec.execute(xor))



if __name__ == "__main__":
    main()
