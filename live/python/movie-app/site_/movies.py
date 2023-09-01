from typing import Optional
from attrs import define, field
from pathlib import Path
import config as cfg
from aiohttp import web

APP_KEY = 'movies.setup.app.classes'

@define(slots=True)
class Movie:
    movie_path: Path = field(converter=Path, eq=False)
    preview_path: Path = field(converter=Path, eq=False)
    thumbnail_path: Path = field(converter=Path, eq=False)
    _float: float = field(init=False, eq=True)
    
    def __attrs_post_init__(self):
        self._float = self.movie_path.stat().st_mtime

    def __hash__(self) -> int:
        return int(self._float * 1000000)
    
    def __eq__(self, mov: 'Movie') -> bool: return float(self) == float(mov)
    def __le__(self, mov: 'Movie') -> bool: return float(self) <= float(mov)
    def __ge__(self, mov: 'Movie') -> bool: return float(self) >= float(mov)
    def __lt__(self, mov: 'Movie') -> bool: return float(self) < float(mov)
    def __gt__(self, mov: 'Movie') -> bool: return float(self) > float(mov)
    def __ne__(self, mov: 'Movie') -> bool: return float(self) != float(mov)

    def json(self):
        return dict(
            movie=self.movie,
            preview=self.preview,
            thumbnail=self.thumbnail,
        )
        
    def json_min(self):
        return self.movie_path.stem

    def __float__(self): return self._float

    @property
    def movie(self):
        return self.movie_path.name

    @property
    def preview(self):
        return self.preview_path.name

    @property
    def thumbnail(self):
        return self.thumbnail_path.name


@define(slots=True, frozen=True)
class _ResourceMaps:
    movies: dict[str, Path]
    previews: dict[str, Path]
    thumbnails: dict[str, Path]

    def create_movies(
        self,
        default_preview: Optional[Path] = None,
        default_thumbnail: Optional[Path] = None,
    ) -> list[Movie]:
        dp = default_preview or cfg.NO_PREVIEW
        dt = default_thumbnail or cfg.NO_THUMBNAIL

        def _construct_movie(stem: str, path: Path):
            p = self.previews.get(stem, dp)
            t = self.thumbnails.get(stem, dt)
            return Movie(movie_path=path, preview_path=p, thumbnail_path=t)

        movies = [_construct_movie(stem, path) for stem, path in self.movies.items()]
        movies.sort(reverse=True)
        return movies


@define(slots=True)
class Movies:
    movie_path: Path = field(converter=Path)
    preview_path: Path = field(converter=Path)
    thumbnail_path: Path = field(converter=Path)
    movies: list[Movie] = field(init=False, factory=list)

    def __attrs_post_init__(self):
        self._load_movies()

    def _load_resource_map(self):
        preview_path = {p.stem: p for p in self.preview_path.iterdir()}
        thumbnail_path = {p.stem: p for p in self.thumbnail_path.iterdir()}
        movies = {p.stem: p for p in self.movie_path.iterdir()}
        return _ResourceMaps(movies, preview_path, thumbnail_path)
    
    def _load_movies(self):
        self.movies = self._load_resource_map().create_movies()

def get_app_movies(app: web.Application) -> Movies:
    movies: Optional[Movies] = app.get(APP_KEY, None)
    if movies is None:
        raise KeyError("Movies was not installed into the application.")
    return movies

def get_movies(req: web.Request) -> Movies:
    return get_app_movies(req.app)

def setup(app: web.Application):
    movies = Movies(cfg.MOVIE_DIR, cfg.PREVIEW_DIR, cfg.THUMBNAIL_DIR)
    app[APP_KEY] = movies
    return movies