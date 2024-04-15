import dataclasses as dt, typing as ty, config as cfg, random, enum
from aiohttp import web
from pathlib import Path

APP_KEY = "movies.app.key.moviesite"

T = ty.TypeVar("T")
Sorter = ty.Callable[[ty.Sequence[T]], ty.Iterable[T]]
PathSortT = Sorter['Movie']


class MovieSorter:
    @staticmethod
    def sort_by_name(items: ty.Sequence["Movie"]):
        return sorted(items, key=lambda movie: str(movie.path))

    @staticmethod
    def _time_sorter(movie: "Movie"):
        return movie.path.stat().st_mtime

    @staticmethod
    def sort_by_time_newest(items: ty.Sequence["Movie"]):
        return sorted(items, key=MovieSorter._time_sorter, reverse=True)

    @staticmethod
    def sort_by_time_oldest(items: ty.Sequence["Movie"]):
        return sorted(items, key=MovieSorter._time_sorter)

    @staticmethod
    def sort_randomly(items: ty.Sequence["Movie"]):
        tmp = list(items)
        random.shuffle(tmp)
        return tmp

    @staticmethod
    def identity(items: ty.Sequence["Movie"]):
        return items

@dt.dataclass
class _Order(str):
    _value: str
    _sorter: PathSortT = MovieSorter.identity

@enum._simple_enum(enum.StrEnum)  # type: ignore
class Order:
    def __new__(cls, order: str, strategy: PathSortT = MovieSorter.identity) -> _Order:
        value = _Order.__new__(cls, order)
        value._value = order
        value._sorter = strategy
        return value

    NONE = "none", MovieSorter.identity
    NEW = "new", MovieSorter.sort_by_time_newest
    OLD = "old", MovieSorter.sort_by_time_oldest
    NAME = "name", MovieSorter.sort_by_name
    RANDOM = "random", MovieSorter.sort_randomly


@dt.dataclass
class Movie:
    path: Path
    movie_id: int = -1

    @dt.dataclass(slots=True)
    class ValidMovie:
        path: "Movie"
        movie: bool = dt.field(init=False, kw_only=True)
        preview: bool = dt.field(init=False, kw_only=True)
        thumbnail: bool = dt.field(init=False, kw_only=True)

        def __post_init__(self):
            self.movie = self.path.movie_path.exists()
            self.thumbnail = self.path.thumbnail_path.exists()
            self.preview = self.path.preview_path.exists()

        def __bool__(self) -> bool:
            return self.preview and self.movie and self.thumbnail

    @property
    def preview(self) -> str:
        return self.path.name

    @property
    def movie(self):
        return self.path.name

    @property
    def thumbnail(self) -> str:
        return f"{self.path.stem}.png"

    @property
    def preview_path(self):
        return cfg.PREVIEW_DIR / self.preview

    @property
    def movie_path(self):
        return cfg.VIDEO_DIR / self.movie

    @property
    def thumbnail_path(self):
        return cfg.THUMBNAIL_DIR / self.thumbnail

    @property
    def valid(self) -> ValidMovie | bool:
        return Movie.ValidMovie(self)

    def json(self) -> dict:
        return dict(
            movie=self.movie,
            thumbnail=self.thumbnail,
            preview=self.preview,
            movie_id=self.movie_id,
        )


class MovieList(list[Movie]):
    def json(self) -> list:
        return [movie.json() for movie in self]


@dt.dataclass
class Movies:
    path: Path
    order: Order
    movies: MovieList = dt.field(init=False)
    total: int = dt.field(init=False)

    def __post_init__(self):
        self.set_movies()

    def sort_movies(self, order: ty.Optional[Order] = None):
        order = self.order if order is None else order
        self.movies = MovieList(order._sorter(self.movies)) # type: ignore
        self.set_movie_ids()

    def set_movie_ids(self):
        for mid, movie in enumerate(self.movies):
            movie.movie_id = mid

    def set_movies(self, order: Order | None = None):
        self.movies = MovieList(Movie(path) for path in self.path.iterdir())
        self.sort_movies(order)
        self.total = len(self.movies)

    def partition(self, offset: int = 0, limit: int = 5):
        return MovieList(self.movies[offset : limit + offset])

    def __len__(self) -> int:
        return self.total


def get_movies(app: web.Application) -> Movies:
    if movies := app.get(APP_KEY):
        return movies
    raise Exception("Movies plugin not setup, call setup(app)")


def movies(req: web.Request) -> Movies:
    return get_movies(req.app)


def setup(app: web.Application, config: cfg.Config):
    movies = Movies(cfg.VIDEO_DIR, Order(config.sort_ordering))  # type:ignore
    app[APP_KEY] = movies
