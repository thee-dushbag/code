from io import StringIO
from time import sleep
from typing import NamedTuple, cast

import faker
import hi
import rich
from rich import box
from rich._spinners import SPINNERS
# from rich.json import JSON
from rich.console import Console, JustifyMethod, OverflowMethod
from rich.status import Status
from rich.table import Column, Table
from rich.text import Text


class MyObject:
    def __str__(self):
        return f"This is MyObject."

    def __rich__(self):
        return f"[green]This is [red]MyObject[white]."


c = Console(style="bold green on black", record=True)
# json_string = '["foofoo", "basketball", "ghali", 20]'
# rich.print_json(json_string)
# rich.print(JSON(json_string))
# rich.print(MyObject())
# # c.out(MyObject(), locals())
# c.rule(Text("[ RIGHT ]"), align='right')
# c.rule(Text("[ CENTER ]"), align='center')
# c.rule(Text("[ LEFT ]"), align='left')

headers = [Column(title.title(), width=50) for title in ["name", "email", "age"]]
table = Table(
    *headers,
    title=Text("Printed table."),
    caption=Text("This is a rich table.", justify="right"),
    box=box.SIMPLE,
)
rows = [
    [Text(name), Text(email), Text(str(age))]
    for name, email, age in (
        ("Simon Nganga", "simongash@gmail.com", 20),
        ("Faith Njeri", "faithnjeri@gmail.com", 10),
    )
]

for row in rows:
    table.add_row(*row)


class ValuesTuple(NamedTuple):
    a: int
    b: str
    c: bytes


def printing():
    c.print("Hello World. This is a [blue underline]link[/blue underline].")
    c.print("A list can be printed to: ", [1, 2, 3, 4])
    c.print("A dict to: ", {"a": 1, "b": 2, "c": 3})
    c.print("A tuple to: ", (1, 2, 3, 4))
    c.print("A set to: ", {1, 2, 3, 4}, style="green on black")
    c.print("A namedtuple to: ", ValuesTuple(5052, "string here", b"bytes here"))
    c.print(table)


def logging():
    name, age = "Simon Nganga", 20
    c.log("Hey There", log_locals=True)


def console_size():
    for i in range(10):
        width, height = c.size
        print(f"terminal_size({width=}, {height=})")
        sleep(1)


def status():
    for spinner in SPINNERS.keys():
        c.print(f"[yellow bold]Spinner[white]:[blue] {spinner}")
        with c.status("Fetching data...", spinner=spinner):
            sleep(2)


def justify_align():
    style = "bold white on purple"
    for justify in ["default", "left", "center", "right", "full"]:
        c.print(f"RichText", style=style, justify=cast(JustifyMethod, justify))


def overflow_():
    supercali = "supercalifragilisticexpialidocious" * 3
    overflows: list[OverflowMethod] = ["fold", "ellipsis", "ignore"]
    for overflow in overflows:
        c.rule(Text(f"Overflow: {overflow!r}"), characters="_")
        c.print(supercali, overflow=overflow, style="bold white")
        c.print()


def prompt():
    name = c.input(":smiley: Your [i]Name[/i]? ")
    hi.say_hi(name)


def record():
    for i in range(1, 6):
        c.print(f"[bold yellow][i]i[/i][white]: [green]{i}")
        sleep(0.5)
    with c.status(
        "[blue bold][i]Counting to [/i][yellow]20...",
        spinner="bouncingBall",
        spinner_style="bold yellow reverse",
    ):
        for i in range(1, 21):
            c.print(f"[bold yellow][i]counter [/i][white]at [green]{i}")
            sleep(0.5)
    from rich.terminal_theme import MONOKAI

    c.print(c.save_svg("rich.svg", title="My Rich Console SVG Recod.", theme=MONOKAI))


def redirection():
    with open("std.txt", "w") as file:
        con = Console(file=file)
        for i in range(10):
            con.print(f"[bold][i]i[/i][white]:[green] {i}")


def pager():
    text = faker.Faker().sentence(10000)
    with c.pager():
        c.print(text)


def alt_screen():
    with c.screen():
        c.print(globals())
        sleep(5)


if __name__ == "__main__":
    alt_screen()
