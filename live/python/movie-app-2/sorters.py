import typing as ty

if ty.TYPE_CHECKING:
    from .movies import Movie
else:
    Movie = None

Sorter = ty.Callable[[list[Movie]], None]


def _name_sorter(movie: Movie):
    return movie.path.name


def _time_sorter(movie: Movie):
    return movie.path.stat().st_mtime


def _size_sorter(movie: Movie):
    return movie.path.stat().st_size


def name(items: list[Movie]):
    items.sort(key=_name_sorter)


def eman(items: list[Movie]):
    items.sort(key=_name_sorter, reverse=True)


def time_newest(items: list[Movie]):
    items.sort(key=_time_sorter, reverse=True)


def time_oldest(items: list[Movie]):
    items.sort(key=_time_sorter)


def size_biggest(items: list[Movie]):
    items.sort(key=_size_sorter, reverse=True)


def size_smallest(items: list[Movie]):
    items.sort(key=_size_sorter)


def randomly(items: list[Movie]):
    import random

    random.shuffle(items)
