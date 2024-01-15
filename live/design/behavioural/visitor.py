import enum, typing as ty, math

# Expression Evaluator


class Token:
    def __init__(self, type: "TokenType", lexeme: str, column: int) -> None:
        self.lexeme = lexeme
        self.type = type
        self.column = column

    def __str__(self) -> str:
        return f"Token({self.type!s}, {self.lexeme!r}, {self.column})"

    __repr__ = __str__


class TokenType(enum.StrEnum):
    NUMBER = enum.auto()
    SLASH = enum.auto()
    MINUS = enum.auto()
    RIGHT = enum.auto()
    POWER = enum.auto()
    STAR = enum.auto()
    FACT = enum.auto()
    PLUS = enum.auto()
    LEFT = enum.auto()
    DOT = enum.auto()
    EOF = enum.auto()


class Lexer:
    def __init__(self, source: str | None = None, /) -> None:
        source = "" if source is None else source
        self._tokens: list[Token] = []
        self._stop = len(source)
        self._source = source
        self._current = 0
        self._start = 0

    def reset(self, src: str | None = None):
        self.__init__(self._source if src is None else src)

    def empty(self) -> bool:
        return self._current >= self._stop

    def add_token(self, type: TokenType):
        lexeme = self._lexeme()
        token = Token(type, lexeme, self._start)
        self._tokens.append(token)

    def _lexeme(self):
        return self._source[self._start : self._current]

    def _scan(self):
        while not self.empty():
            match self.peek():
                case " ":
                    self.consume_char()
                case ".":
                    self.consume_char(TokenType.DOT)
                case "*":
                    self.consume_char(TokenType.STAR)
                case "-":
                    self.consume_char(TokenType.MINUS)
                case "/":
                    self.consume_char(TokenType.SLASH)
                case "+":
                    self.consume_char(TokenType.PLUS)
                case "^":
                    self.consume_char(TokenType.POWER)
                case "(":
                    self.consume_char(TokenType.LEFT)
                case "!":
                    self.consume_char(TokenType.FACT)
                case ")":
                    self.consume_char(TokenType.RIGHT)
                case char:
                    if char.isdigit():
                        self.consume_number()
                        continue
                    raise Exception(f"Invalid character {char!r}")

    def scan(self, src: str | None = None):
        self.reset(src)
        self._scan()
        self.add_token(TokenType.EOF)
        return self._tokens

    def peek(self) -> str:
        return "" if self.empty() else self._source[self._current]

    def advance(self):
        self._current += 1

    def consume(self):
        self._start = self._current

    def consume_token(self, type: TokenType):
        self.add_token(type)
        self.consume()

    def consume_number(self):
        while self.peek().isdigit():
            self.advance()
        self.consume_token(TokenType.NUMBER)

    def consume_char(self, type: TokenType | None = None):
        self.advance()
        if type is not None:
            self.consume_token(type)
        else:
            self.consume()


class Expression(ty.Protocol):
    def accept(self, visitor: "Visitor") -> ty.Any:
        ...


class Binary:
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.right = right
        self.left = left
        self.operator = operator


class PreUnary:
    def __init__(self, operator: Token, right: Expression) -> None:
        self.right = right
        self.operator = operator


class PostUnary:
    def __init__(self, left: Expression, operator: Token) -> None:
        self.operator = operator
        self.left = left


class PrePost_ry:
    def __init__(self, pre: Token, middle: Expression, post: Token) -> None:
        self.middle = middle
        self.post = post
        self.pre = pre


class Plus(Binary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_plus(self)


class Minus(Binary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_minus(self)


class Slash(Binary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_slash(self)


class Star(Binary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_star(self)


class Power(Binary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_power(self)


class Number(Expression):
    def __init__(self, number: Token) -> None:
        self.number = number

    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_number(self)


class Group(PrePost_ry, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_group(self)


class UnaryPlus(PreUnary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_unary_plus(self)


class UnaryMinus(PreUnary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_unary_minus(self)


class Factorial(PostUnary, Expression):
    def accept(self, visitor: "Visitor") -> ty.Any:
        return visitor.accept_factorial(self)


class Visitor(ty.Protocol):
    def accept_plus(self, plus: Plus):
        ...

    def accept_star(self, star: Star):
        ...

    def accept_minus(self, minus: Minus):
        ...

    def accept_slash(self, slash: Slash):
        ...

    def accept_group(self, group: Group):
        ...

    def accept_power(self, power: Power):
        ...

    def accept_number(self, number: Number):
        ...

    def accept_unary_minus(self, unary_minus: UnaryMinus):
        ...

    def accept_unary_plus(self, unary_plus: UnaryPlus):
        ...

    def accept_factorial(self, factorial: Factorial):
        ...

    def visit(self, root: Expression):
        ...


class Parser:
    def __init__(self, tokens: list[Token] | None = None) -> None:
        self._tokens = tokens or []
        self._current = 0

    def expression(self):
        return self.term()

    def term(self):
        left = self.factor()
        match self.peek().type:
            case TokenType.PLUS:
                operator = self.advance()
                right = self.term()
                return Plus(left, operator, right)
            case TokenType.MINUS:
                operator = self.advance()
                right = self.term()
                return Minus(left, operator, right)
        return left

    def factor(self):
        left = self.fact()
        match self.peek().type:
            case TokenType.SLASH:
                operator = self.advance()
                right = self.factor()
                return Slash(left, operator, right)
            case TokenType.STAR:
                operator = self.advance()
                right = self.factor()
                return Star(left, operator, right)
        return left

    def fact(self):
        left = self.unary()
        while self.peek().type == TokenType.FACT:
            operator = self.advance()
            left = Factorial(left, operator)
        return left

    def unary(self):
        match self.peek().type:
            case TokenType.MINUS:
                operator = self.advance()
                right = self.unary()
                return UnaryMinus(operator, right)
            case TokenType.PLUS:
                operator = self.advance()
                right = self.unary()
                return UnaryPlus(operator, right)
        return self.power()

    def power(self):
        left = self.prepost()
        while self.peek().type == TokenType.POWER:
            operator = self.advance()
            right = self.prepost()
            left = Power(left, operator, right)
        return left

    def prepost(self):
        if self.peek().type == TokenType.LEFT:
            pre = self.advance()
            middle = self.expression()
            post = self.consume(
                TokenType.RIGHT,
                f"Expected ')' to close group expression at {pre.column}",
            )
            return Group(pre, middle, post)
        return self.primary()

    def primary(self):
        if self.peek().type == TokenType.NUMBER:
            number = self.advance()
            if self.match(TokenType.DOT):
                n = self.consume(TokenType.NUMBER, "Expected a number after the dot.")
                number.lexeme += "." + n.lexeme
            return Number(number)
        raise Exception(f"Expected a number, got {self.peek()!s}")

    def consume(self, type: TokenType, msg: str):
        if self.peek().type != type:
            raise Exception(msg)
        return self.advance()

    def empty(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self._tokens[self._current]

    def advance(self):
        last = self.peek()
        self._current += 1
        return last

    def match(self, *types: TokenType):
        _type = self.peek().type
        for type in types:
            if _type == type:
                self.advance()
                return True
        return False

    def reset(self, tokens: list[Token] | None = None):
        self.__init__(self._tokens if tokens is None else tokens)

    def parse(self, tokens: list[Token] | None = None):
        self.reset(tokens)
        return self.expression()


class Interpreter(Visitor):
    def accept_number(self, number: Number):
        type = float if "." in number.number.lexeme else int
        return type(number.number.lexeme)

    def accept_plus(self, plus: Plus):
        left = plus.left.accept(self)
        right = plus.right.accept(self)
        return right + left

    def accept_minus(self, minus: Minus):
        left = minus.left.accept(self)
        right = minus.right.accept(self)
        return right - left

    def accept_power(self, power: Power):
        left = power.left.accept(self)
        right = power.right.accept(self)
        return pow(left, right)

    def accept_star(self, star: Star):
        left = star.left.accept(self)
        right = star.right.accept(self)
        return right * left

    def accept_group(self, group: Group):
        return group.middle.accept(self)

    def accept_slash(self, slash: Slash):
        left = slash.left.accept(self)
        right = slash.right.accept(self)
        if right == 0:
            raise ZeroDivisionError(
                f"Slash at column {slash.operator.column}, '{left} / 0'"
            )
        return left / right

    def accept_unary_minus(self, unary_minus: UnaryMinus):
        return -unary_minus.right.accept(self)

    def accept_unary_plus(self, unary_plus: UnaryPlus):
        return +unary_plus.right.accept(self)

    def accept_factorial(self, factorial: Factorial):
        left = int(factorial.left.accept(self))
        return math.factorial(left)

    def interpret(self, root: Expression):
        return root.accept(self)

    visit = interpret


class Debugger(Visitor):
    def __init__(self, parens=None) -> None:
        self._parens = parens or False

    def _p(self, s: str):
        if self._parens:
            return f"({s})"
        return s

    def accept_group(self, group: Group):
        ps = "(", ")"
        if self._parens:
            ps = "", ""
        return ps[0] + group.middle.accept(self) + ps[1]

    def _lr(self, binary: Binary):
        left = binary.left.accept(self)
        right = binary.right.accept(self)
        return left, right

    def accept_minus(self, minus: Minus):
        l, r = self._lr(minus)
        return self._p(f"{l} - {r}")

    def accept_plus(self, plus: Plus):
        l, r = self._lr(plus)
        return self._p(f"{l} + {r}")

    def accept_star(self, star: Star):
        l, r = self._lr(star)
        return self._p(f"{l} * {r}")

    def accept_power(self, power: Power):
        l, r = self._lr(power)
        return self._p(f"{l} ^ {r}")

    def accept_slash(self, slash: Slash):
        l, r = self._lr(slash)
        return self._p(f"{l} / {r}")

    def accept_factorial(self, factorial: Factorial):
        return self._p(f"{factorial.left.accept(self)}!")

    def accept_number(self, number: Number):
        print(number.number.lexeme)
        return number.number.lexeme

    def accept_unary_minus(self, unary_minus: UnaryMinus):
        return self._p(f"-{unary_minus.right.accept(self)}")

    def accept_unary_plus(self, unary_plus: UnaryPlus):
        return self._p(f"+{unary_plus.right.accept(self)}")

    def debug(self, root: Expression):
        return root.accept(self)

    visit = debug


def main():
    expr = "100 - 2 ^ 4 / (2 - 4 ^ 0.5) + 9 / 7"

    # Expression Evaluation Pipeline
    lexer = Lexer()
    tokens = lexer.scan(expr)

    parser = Parser()
    ast = parser.parse(tokens)

    interpreter = Interpreter()
    reuslt = interpreter.interpret(ast)

    print(reuslt)


if __name__ == "__main__":
    main()
