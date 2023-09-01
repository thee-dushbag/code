import click
from rich.console import Console
from rich.progress import track
from time import sleep

console = Console()

@click.command('greet')
@click.option("--name", '-n', help="Say hi to <NAME>", required=True)
def say_hi(name: str):
    """This function enables you to say hi to someone named <NAME> [provided]"""
    console.print(f"[bold blue]Hello [italic][yellow]{name}[/italic][blue], how was your day[purple]?")

@click.command('count_to')
@click.argument('n', type=int, default=10)
@click.option('--bar/--no-bar', ' /-b', default=True)
@click.option('--delay', '-d', default=.1, type=float)
def counter(n: int, delay: float, bar: bool):
    """Count from 0 to <N> [default=10]. Show progress by --bar/--no-bar"""
    desc = "[white bold]Count at[red]: [italic green3]{i}"
    rng = track(range(n), description="Counting...", console=console) if bar else range(n)
    for i in rng:
        console.print(desc.format(i=i))
        sleep(delay)

if __name__ == '__main__':
    cli = click.Group('cli')
    cli.help = "This is the click argparser and it is amazing."
    cli.add_command(say_hi)
    cli.add_command(counter)
    cli()