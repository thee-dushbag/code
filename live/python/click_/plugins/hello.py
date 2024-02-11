import click

@click.command
@click.argument('name')
def __command__(name: str):
    click.echo("Hello %s, how was your day?" % name)
