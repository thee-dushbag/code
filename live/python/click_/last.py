import click

SETTINGS = dict(help_option_names=["-?", "--help-me"])


@click.command
def hello():
    click.echo("Hello World")


@click.command
@click.pass_context
def from_click(ctx: click.Context):
    click.echo("Greetings from click.")
    ctx.invoke(hello)


if __name__ == "__main__":
    grp = click.Group(
        "grp",
        commands=[hello, from_click],
        help="Just saying hi",
        context_settings=SETTINGS,
        invoke_without_command=True,
        callback=lambda: click.echo("MAIN FUNCTION")
    )
    grp()
