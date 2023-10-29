import click
from .main import application
from aiohttp import web

@click.command
@click.help_option('--help', '-h')
@click.option('--host')
@click.option('--port')
def main(port: int, host: str):
    if port is None: port = 9080
    if host is None: host = 'localhost'
    web.run_app(application(), host=host, port=port)

if __name__ == '__main__':
    main()
