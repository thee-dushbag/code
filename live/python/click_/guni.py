import click

app = click.Group()

@app.command
@click.option(
    "--count",
    default=1,
    help="Number of greetings.",
    type=click.IntRange(0, float("inf"), min_open=False),
)
@click.option(
    "--name", prompt="Target Name", help="Person to be greeted.", type=click.STRING
)
def hello(count: int, name: str):
    "Simple program that greets NAME for a total of COUNT times."
    for _ in range(count):
        click.echo(f"Hello {name}!")


@app.command
@click.option("verbosity", "--verbose", "-v", count=True)
def verbose(verbosity: int):
    click.echo("Verbosity Level: %s" % verbosity)


@app.command
@click.option("--names", "-n", multiple=True)
def names(names: list[str]):
    for name in names:
        print("Hello %s!" % name)


_ = "<NO_NAME>"


@app.command
@click.option("--name", "-n", nargs=2)
@click.option("--brother", "name", flag_value=("Simon", "Nganga"), type=tuple)
@click.option("--friend", "name", flag_value=("Darius", "Kimani"), type=tuple)
@click.option("--sister", "name", flag_value=("Faith", "Njeri"), type=tuple)
@click.option("--mum", "name", flag_value=("Lydia", "Wanjiru"), type=tuple)
@click.option("--dad", "name", flag_value=("Charles", "Njoroge"), type=tuple)
def name(name: tuple[str, str] | None):
    name = (_, _) if name is None else name
    click.echo("Your names are %r and %r." % name)


@app.command
@click.option("--shout/--no-shout", "-s/-S", default=False)
@click.option("--style", "-c", is_flag=True, default=False)
@click.argument("name")
def hey(name: str, shout: bool, style):
    upper = lambda s: s.upper() if shout else s
    tokens = [upper("Hello "), upper(name), "!" + "!" * shout * 2]
    yellow, green, noclr = "\x1b[93;1m", "\x1b[92;1m", "\x1b[0m"
    for token in zip(range(3, -1, -1), (noclr, green, yellow, green)):
        tokens.insert(*token)
    click.echo("".join(tokens), color=style)


# Feature Switch
@app.command
@click.option("--name", type=str)
@click.option("-m", "gender", flag_value="male")
@click.option("-f", "gender", flag_value="female")
@click.option("--gender", type=click.Choice(["male", "female"]), prompt=True)
def data(gender: str, name: str):
    click.echo("%s, you are a %r" % (name, gender))


if __name__ == "__main__":
    app()
