from base64 import urlsafe_b64decode, urlsafe_b64encode
import click

@click.group("b64")
def cli():
    "Terminal Tool for base64 encoding and decoding."

@click.command('decode')
@click.help_option('--help', '-h')
@click.option('--string', '-s', multiple=True)
def decode(string: tuple[str]):
    for encoded in string:
        try:
            value = urlsafe_b64decode(encoded).decode()
            click.echo(value)
        except Exception as e:
            click.echo(f"Error decoding {encoded!r}: {e!s}", err=True)

@click.command('encode')
@click.help_option('--help', '-h')
@click.option('--string', '-s', multiple=True)
def encode(string: tuple[str]):
    for decoded in string:
        try:
            value = urlsafe_b64encode(decoded.encode()).decode()
            click.echo(value)
        except Exception as e:
            click.echo(f"Error encoding {decoded!r}: {e!s}", err=True)

if __name__ == '__main__':
    cli.add_command(decode)
    cli.add_command(encode)
    cli()
