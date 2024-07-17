import enum
from functools import cached_property
import dataclasses as dt, typing as ty, config as cfg
from aiohttp import web
from pathlib import Path
import sorters as sort

APP_KEY = "movies.app.key.moviesite"

T = ty.TypeVar("T")


@dt.dataclass(slots=True)
class _Order:
    value: str
    sorter: sort.Sorter

    def __str__(self):
        return self.value

    __repr__ = __str__


class Order:
    def __new__(cls, order: str) -> _Order:
        return getattr(cls, order.upper())

    @classmethod
    def orders(cls):
        if cls._cached is None:
            cls._cached = {
                name: value
                for name, value in cls.__dict__.items()
                if isinstance(value, _Order)
            }
        return cls._cached.values()

    _cached: dict[str, _Order] | None = None

    NAME = _Order("name", sort.name)
    NEW = _Order("new", sort.time_newest)
    OLD = _Order("old", sort.time_oldest)
    BIG = _Order("big", sort.size_biggest)
    RANDOM = _Order("random", sort.randomly)
    SMALL = _Order("small", sort.size_smallest)
    EMAN = _Order("eman", sort.eman)


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
    order: _Order
    movies: MovieList = dt.field(init=False)
    total: int = dt.field(init=False)

    def __post_init__(self):
        self.set_movies()

    def sort_movies(self, order: ty.Optional[_Order] = None):
        order = self.order if order is None else order
        order.sorter(self.movies)  # type: ignore
        self.set_movie_ids()

    def set_movie_ids(self):
        for mid, movie in enumerate(self.movies):
            movie.movie_id = mid

    def set_movies(self, order: _Order | None = None):
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
