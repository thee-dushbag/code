from dataclasses import dataclass
from pathlib import Path
from typing import Callable, NamedTuple
from string import Template
from itertools import count
from yaml import safe_load as yaml_loader
from json import load as json_loader

SCEHAME_FILE_NAME = "_context_schema.json"


@dataclass(kw_only=True)
class Context:
    file_template: Template
    filelist: list[str]
    output_dir: Path
    episodes_per_season: list[int] | int
    ignore_suffix: str = ".dummy"
    season_dir_template: Template = Template("season_$season")

    def __post_init__(self):
        self._prepare()

    def _prepare(self):
        if isinstance(self.filelist, str):
            path = Path(self.filelist)
            assert path.exists(), "Filelist file was not found..."
            self.filelist = [line for line in path.read_text().splitlines() if line]
        if isinstance(self.file_template, str):
            self.file_template = Template(self.file_template)
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir).absolute()
        if isinstance(self.season_dir_template, str):
            self.season_dir_template = Template(self.season_dir_template)


class SnEp(NamedTuple):
    season: int
    episode: int


def get_dir(ctx: Context, season: int) -> Path:
    if season == 0:
        return ctx.output_dir
    path = ctx.output_dir / ctx.season_dir_template.substitute(season=season)
    if not path.exists():
        path.mkdir(parents=True)
    return path


def _get_file_name(ctx: Context, path: Path, snep: SnEp):
    stem = ctx.file_template.substitute(season=snep.season, episode=snep.episode)
    return path.rename(path.with_stem(stem))


def move_file(ctx: Context, path: Path, snep: SnEp):
    if path.suffix == ctx.ignore_suffix or snep.episode == 0:
        return
    npath = _get_file_name(ctx, path, snep)
    dest = get_dir(ctx, snep.season) / npath.name
    npath.rename(dest)


def season_iterator(episodes_per_season: list[SnEp]):
    for season, episodes in episodes_per_season:
        for episode in range(1, episodes + 1):
            yield SnEp(season, episode)


def _assert_correctness(episodes: list[SnEp], ctx: Context):
    paths = [Path(file).absolute() for file in ctx.filelist]
    for path in paths:
        if path.suffix == ctx.ignore_suffix:
            continue
        assert path.exists(), f"Episode Not Found: {path!r}"
    total_episodes = sum(e for _, e in episodes)
    assert total_episodes == (
        count := len(ctx.filelist)
    ), f"Episodes found {count}, expected {total_episodes}"
    return paths


def _resolve_episodes(episodes: list[int] | int) -> list[SnEp]:
    if isinstance(episodes, int):
        return [SnEp(0, episodes)]
    return [SnEp(s, e) for s, e in zip(count(1), episodes)]


def _validate_config(config: dict):
    from pathlib import Path
    from jsonschema.validators import validator_for
    from json import loads

    schema_file = Path(__file__).resolve().parent / SCEHAME_FILE_NAME
    schema = loads(schema_file.read_text())
    Validator = validator_for(schema)
    validator = Validator(schema)
    validator.validate(config)


def _load_config(config_file: Path, loader: Callable, key=None):
    with config_file.open() as file:
        config = loader(file)
    if key is not None:
        config = config[key]
    _validate_config(config)
    return Context(**config)


def load_yaml_config(config_file: str, *, key=None):
    return _load_config(Path(config_file), yaml_loader, key)


def load_json_config(config_file: str, *, key=None):
    return _load_config(Path(config_file), json_loader, key)


def run(ctx: Context):
    episodes_per_season = _resolve_episodes(ctx.episodes_per_season)
    paths = _assert_correctness(episodes_per_season, ctx)
    for snep, path in zip(season_iterator(episodes_per_season), paths):
        move_file(ctx, path, snep)
