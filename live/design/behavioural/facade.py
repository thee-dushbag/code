from visitor import Interpreter, Debugger, Parser, Lexer


class Evaluator:
    def __init__(self, parens=None) -> None:
        self.interpreter = Interpreter()
        self.debugger = Debugger(parens)
        self.parser = Parser()
        self.lexer = Lexer()

    def _genast(self, src: str):
        if src:
            tokens = self.lexer.scan(src)
            return self.parser.parse(tokens)

    def eval(self, src: str):
        ast = self._genast(src)
        if ast is None:
            return
        return self.interpreter.interpret(ast)

    def show(self, src: str):
        ast = self._genast(src)
        if ast is None:
            return
        debug = self.debugger.debug(ast)
        result = self.interpreter.interpret(ast)
        return f"{debug} = {result}"


def main():
    # Hide away the evaluation pipeline
    # and provide a simple interface

    expr = "100 - 2 ^ 4 / (2 - 4 ^ 0.5) + 9 / 7"
    calc = Evaluator()  # Facade Class
    print(calc.eval(expr))


if __name__ == "__main__":
    ...
