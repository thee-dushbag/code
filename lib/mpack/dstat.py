import dataclasses as dt
import typing as ty
from functools import reduce
from pathlib import Path

import click
from mpack.bsize import Bytes

_identity = lambda _, __: None
_add = lambda x, y: x + y
OperateType = ty.Callable[[Path, Bytes], None]

__all__ = "PathSize", "OperateType", "cli"


@dt.dataclass(slots=True)
class PathSize:
    operate: OperateType = _identity
    follow_symlinks: bool = dt.field(default=False, kw_only=True)
    block_size: bool = dt.field(default=False, kw_only=True)

    def _file_size(self, path: Path) -> Bytes:
        stat = path.stat(follow_symlinks=self.follow_symlinks)
        blk_size = stat.st_blksize if self.block_size else 0
        return Bytes(stat.st_size) + blk_size

    def _dir_size(self, path: Path) -> Bytes:
        blk_size = path.stat().st_blksize if self.block_size else 0

        def _size(sub_path: Path) -> Bytes:
            getsize = self._dir_size if sub_path.is_dir() else self._file_size
            size = getsize(sub_path)
            self.operate(sub_path, size)
            return size

        sizes = [_size(p) for p in path.iterdir()]
        if not sizes:
            return Bytes() + blk_size
        return reduce(_add, sizes) + blk_size

    def __call__(self, path: Path | str, *, operate: bool = False) -> Bytes:
        if isinstance(path, str):
            path = Path(path)
        assert path.exists(), f"File Not Found: {path!r}"
        return self.getsize(path, operate=operate)

    def getsize(self, path: Path, *, operate: bool = True) -> Bytes:
        getsize = self._dir_size if path.is_dir() else self._file_size
        size = getsize(path)
        if operate:
            self.operate(path, size)
        return size


DEFAULT_FORMAT = "[%gGB %mMB %kKB %bbytes]: %p"


def log_operate(format_spec: str, *, log: bool):
    def operate(path: Path, size: Bytes):
        string = format_spec.replace("%p", str(path))
        click.echo(format(size, string))

    return operate if log else _identity


@click.command
@click.argument("spath", type=click.Path(exists=True))
@click.option("--format", "-F", default=DEFAULT_FORMAT)
@click.option("--follow-symlinks", "-f", is_flag=True)
@click.option("--block-size", "-b", is_flag=True)
@click.option("--log", "-l", is_flag=True)
def cli(
    format: str,
    log: bool,
    block_size: bool,
    follow_symlinks: bool,
    spath: str,
):
    operate = log_operate(format, log=log)
    pathsize = PathSize(operate, follow_symlinks=follow_symlinks, block_size=block_size)
    path = Path(spath)
    size = pathsize(path)
    logger = log_operate(DEFAULT_FORMAT, log=True)
    logger(path, size)


if __name__ == "__main__":
    cli()
