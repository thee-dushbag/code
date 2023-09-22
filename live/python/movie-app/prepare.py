import asyncio as aio
from pathlib import Path

from moviepy.editor import VideoFileClip

CONTENT_DIR = Path.home() / "Content"
RESOURCE_DIR = CONTENT_DIR / ".bin" / "resources"
MOVIEAPP_DIR = RESOURCE_DIR / "movie-app"

MOVIE_DIR = MOVIEAPP_DIR / "movies"
THUMBNAIL_DIR = MOVIEAPP_DIR / "thumbnails"
PREVIEW_DIR = MOVIEAPP_DIR / "previews"

for dir in (THUMBNAIL_DIR, MOVIE_DIR, PREVIEW_DIR):
    if not dir.exists():
        dir.mkdir()


def create_thumbnails(movies: list[Path]):
    for movie in movies:
        thumbnail = THUMBNAIL_DIR / movie.with_suffix(".png").name
        if thumbnail.exists():
            continue
        movie_clip = VideoFileClip(str(movie))
        t = int(movie_clip.duration / 4)
        movie_clip.save_frame(str(thumbnail), t)


async def create_previews(movies: list[Path]):
    from mpack.preview import Previews

    not_found = list(mov for mov in movies if not (PREVIEW_DIR / mov.name).exists())
    if not not_found:
        return
    previews = Previews(not_found, PREVIEW_DIR)
    await previews.create_async(img_cnt=15)


movies = list(MOVIE_DIR.iterdir())


async def create_all(movies):
    loop = aio.get_event_loop()
    task = loop.run_in_executor(None, create_thumbnails, movies)
    task2 = create_previews(movies)
    rs = await aio.gather(task, task2, return_exceptions=True)
    for r in rs:
        if isinstance(r, BaseException):
            print("Error: " + str(r))


aio.run(create_all(movies))
