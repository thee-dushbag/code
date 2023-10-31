import functools
import click, typing as ty

ShifterType: ty.TypeAlias = ty.Callable[[str, int], str]


def shiftchar(char: str, length: int) -> str:
    return chr(ord(char) + length)

def shift_range(start_char: str, size: int) -> ShifterType:
    S = ord(start_char)
    _t = lambda c: S <= c < (S + size)

    def _shifter(char: str, length: int):
        c = ord(char)
        v = (((c + length - S) % size) + S) if _t(c) else c
        return chr(v)

    return _shifter


upper_letter_shift = shift_range("A", 26)
lower_letter_shift = shift_range("a", 26)


def shiftletters(text: str, length: int):
    upper_shift = functools.partial(upper_letter_shift, length=length)  # type: ignore
    lower_shift = functools.partial(lower_letter_shift, length=length)  # type: ignore
    text = "".join(map(lower_shift, text))  # type: ignore
    return "".join(map(upper_shift, text))  # type: ignore


@click.command
@click.argument("text", type=str, default=None)
@click.option("--length", "-l", default=3, type=int, help="Length to shift chars by.")
def cli(text: str, length: int):
    if text is None: text = input()
    ntext = shiftletters(text, length)
    click.echo(ntext)


if __name__ == "__main__":
    cli()
