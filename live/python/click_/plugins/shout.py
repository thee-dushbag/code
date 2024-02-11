import click

@click.command
@click.option("words", '--word', '-w', multiple=True, type=str)
def __command__(words: tuple[str]):
    if not words:
        return
    click.echo("WORDS:")
    for count, word in enumerate(words, start=1):
        click.echo(" %s. %s!!!" % (count, word.upper()))
