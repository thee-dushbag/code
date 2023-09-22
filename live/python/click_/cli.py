from time import sleep

import click


def say_hi(name: str) -> str:
    return f"Hello {name}, how was your day?"


@click.command("hello")
@click.option("--count", default=1, help="Number of Greetings")
@click.option("--name", prompt="Your Name", help="Name of Person to Greet")
def hello(count: int, name: str):
    for _ in range(count):
        click.echo(say_hi(name))


@click.command("progress")
@click.option("--start", default=1)
@click.option("--stop", default=100)
@click.option("--step", default=1)
@click.option("--delay", default=0.5)
def progress_bar(start: int, stop: int, step: int, delay: float):
    with click.progressbar(range(start, stop, step)) as bar:
        for i in bar:
            # click.echo(f"i: {i}", nl=False)
            sleep(delay)


cli = click.Group("cli")
cli.help = "This is me learning click"
cli.add_command(progress_bar)
cli.add_command(hello)


@cli.command("say-what")
def say_what():
    click.echo("Say Whaaaat, Motherfucker.")


@cli.command("names")
# @click.argument("names", nargs=3, type=str)
@click.option("--names", nargs=3, type=str, prompt="Your names please")
def enter_names(names):
    click.echo(f"You entered: {names}")
    click.echo(f"Your First name is  : {names[0]!r}")
    click.echo(f"Your Second name is : {names[1]!r}")
    click.echo(f"Your Third name is  : {names[2]!r}")


@cli.command("mult")
@click.option("--val", "-v", multiple=True)
def multi(val):
    click.echo(f"Received: {val}")


@cli.command("bool_flag")
@click.option("--debug/--no-debug", default=False)
def debugy(debug):
    click.echo(f"debug set to {debug}")


@cli.command("count")
@click.option("-c", "--cnt", count=True)
def count(cnt):
    click.echo(f"We have counted -c at {cnt}")


@cli.command("my_gender")
@click.option(
    "--gender", prompt="What is your gender", type=click.Choice(["male", "woman"])
)
def what_gender(gender: str):
    click.confirm("Please confirm entered gender")
    t = "man" if gender.lower() == "male" else "woman"
    print(f"Your are a {t.title()}")


@cli.command("db")
@click.option("--db-url", "-U", type=str, prompt=True)
# @click.option("--password", "-p", hide_input=False, confirmation_prompt=True, prompt=True)
@click.password_option()
def connect(password, db_url):
    click.echo(f"Connecting to database with {password=} at {db_url=}")


@cli.command("drop")
@click.option("--yes", "-y", prompt="Are you sure", default=False, is_flag=True)
# @click.confirmation_option(prompt="Are you sure")
def drop_db(yes):
    if yes:
        click.echo("Dropping database!")


class sentinel:
    ...


s = sentinel()


@cli.command("exp")
@click.option("--val", expose_value=True)
def expose(val=None):
    val = val or s
    click.echo(f"Exposed value: {val}")


@cli.command("pth")
@click.option("paths", "--path", "-p", multiple=True, type=click.Path(exists=True))
def paths(paths):
    for path in paths:
        click.echo(path)


if __name__ == "__main__":
    cli()
