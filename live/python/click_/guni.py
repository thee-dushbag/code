from typing import Sequence

import click as cli


@cli.command
@cli.option("-m", "--method", default="GET")
@cli.argument("url")
def httpx(url: str, method: str):
    print(f"Method: {method}")
    print(f"Url: {url}")


if __name__ == "__main__":
    from sys import argv

    httpx(*argv)
