from ._nameep import load_json_config, load_yaml_config, run, Context
from typing import cast
from pathlib import Path
import click

_loaders = dict(yaml=load_yaml_config, json=load_json_config)
_working_dir = Path(__file__).resolve().parent
_template_dir = _working_dir / 'template'

class SnEpParam(click.ParamType):
    name = "SnEpParam"

    def convert(self, value: str, param, ctx) -> list[int] | int:
        eps = [v.strip() for v in value.split(",") if v]
        if len(eps) == 0:
            self.fail("You passed no episodes what's so ever.", param, ctx)
        if not all(e.isnumeric() for e in eps):
            self.fail(
                "Expected the episodes to be a comma separated string of integers: '1,2,3,4,4'",
                param,
                ctx,
            )
        eps = [int(e) for e in eps]
        if len(eps) == 1 and "," not in value:
            return eps[0]
        return eps


@click.group
def _cli():
    'Application for renaming unordered episodes in a folder or filelist.'


@_cli.command
@click.argument("filelist", type=click.Path(exists=True, dir_okay=False))
@click.option("--episodes-per-season", "-e", type=SnEpParam(), prompt=True)
@click.option(
    "--season-dir-template",
    "-s",
    default=Context.season_dir_template.template,
    prompt=True,
)
@click.option("--file-template", "-f", prompt=True)
@click.option(
    "--output-dir", "-o", type=click.Path(exists=False, file_okay=False), prompt=True
)
def cli(
    filelist: str,
    episodes_per_season: list[int] | int,
    season_dir_template: str,
    file_template: str,
    output_dir: str,
):
    ctx = Context(
        file_template=file_template,  # type: ignore
        filelist=filelist,  # type: ignore
        output_dir=output_dir,  # type: ignore
        episodes_per_season=episodes_per_season,
        season_dir_template=season_dir_template,  # type: ignore
    )
    run(ctx)


@_cli.command
@click.argument("config", type=click.Path(exists=True, dir_okay=False))
@click.option("--type", default="yaml", type=click.Choice(["json", "yaml"]))
def config(config: click.File, type: str):
    loader = _loaders[type]
    run(loader(cast(str, config)))

def _get_template(type: str, bare: bool = False) -> Path:
    sbare = 'bare.' if bare else ''
    template = sbare + f'template.{type}'
    return _template_dir / template

@_cli.command
@click.argument('output', type=click.Path(dir_okay=False))
@click.option('--type', '-t', type=click.Choice(['json', 'yaml']), default=None)
@click.option('--bare', '-b', is_flag=True)
def template(output: str, type: str, bare: bool):
    path = Path(output)
    if type is None:
        if path.suffix == '.json':
            type = 'json'
        elif path.suffix in ['.yaml', '.yml']:
            type = 'yaml'
        else:
            type = 'yaml'
    file = _get_template(type, bare)
    if not path.exists(): path.touch()
    path.write_text(file.read_text())