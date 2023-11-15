import click

from ..dstat import cli as dstat_command
from ..nameep import cli as nameep_group
from ..toxspf import make_playlist as make_playlist_command
from ..webrun import main as webrun_command
from .msort import msort as sort_command
from ..b64 import decode as b64_decode, encode as b64_encode


# Base Container for the command line tools ...
@click.group
def cli():
    "My Command line python tools"

# Register the commands ...
cli.add_command(make_playlist_command, "toxspf")
cli.add_command(webrun_command, "webrun")
cli.add_command(dstat_command, "dstat")
cli.add_command(nameep_group, "nameep")
cli.add_command(sort_command, "sort")
cli.add_command(b64_decode, 'b64.decode')
cli.add_command(b64_encode, 'b64.encode')