import click
from .msort import msort as msort_command

@click.group
def cli():
    'My Command line python tools'

cli.add_command(msort_command, 'sort')