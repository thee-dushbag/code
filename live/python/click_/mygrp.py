from pathlib import Path
import click, importlib

plugin_dir = Path(__file__).parent / "plugins"


class PluginCommand(click.MultiCommand):
    def list_commands(self, ctx: click.Context) -> list[str]:
        plugins = importlib.import_module(plugin_dir.name)
        return plugins.__plugins__

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        plugins = importlib.import_module(plugin_dir.name)
        if cmd_name not in plugins.__plugins__:
            return
        plugin = getattr(plugins, cmd_name, None)
        if plugin is None:
            return
        return getattr(plugin, "__command__", None)


@click.command(cls=PluginCommand)
def plugins():
    ...


@click.group
def cli():
    ...


@cli.command
@click.argument("name")
@click.option("--upper", "transform", flag_value="upper")
@click.option("--title", "transform", flag_value="title", default=True)
@click.option("--cap", "transform", flag_value="capitalize")
@click.option("--lower", "transform", flag_value="lower")
def hey(name: str, transform):
    transform = getattr(str, transform)
    click.echo("Hey %s!!!" % transform(name))


coll = click.CommandCollection("coll", sources=[cli, plugins])

if __name__ == "__main__":
    coll()
