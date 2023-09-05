from ..toxspf import make_playlist as make_playlist_command
from ..webrun import main as webrun_command
from .msort import msort as sort_command
from ..nameep import cli as nameep_group
import click

# Base Container for the command line tools ...
@click.group
def cli():
    'My Command line python tools'

# Register the commands ...
cli.add_command(make_playlist_command, 'toxspf')
cli.add_command(webrun_command, 'webrun')
cli.add_command(nameep_group, 'nameep')
cli.add_command(sort_command, 'sort')