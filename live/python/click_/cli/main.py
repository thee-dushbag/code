import click

TEMPLATE = "Hello %s, how was your day?"


def greet(name: str, template: str | None = None) -> str:
    return (template or TEMPLATE) % name


@click.command("greet")
@click.argument("name", type=str, default='stranger')
@click.option("--template", "-t")
@click.pass_context
def greet_cli(ctx: click.Context, name: str, template: str | None):
    if template is not None and template.count("%") != 1:
        ctx.fail("Invalid template: Must contain the placeholder like %s/%r.")
    click.echo(greet(name.title(), template))
