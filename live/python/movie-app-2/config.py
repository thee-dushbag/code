from css_html_js_minify.minify import process_multiple_files
import typing as ty, dataclasses as dt, tempfile as tmp
from concurrent.futures import ThreadPoolExecutor, wait
from mpack.previews import Preview, _DEFAULT
from pathlib import Path
from aiohttp import web

# Main contants
APP_KEY: ty.Final = "movie.site.configurations"
WORKING_DIR: ty.Final = Path(__file__).parent

# Statics directories
STATIC_DIR = WORKING_DIR / "static"
PUBLIC_DIR = WORKING_DIR / "public"
TEMPLATE_DIR = WORKING_DIR / "templates"

# App resources
RESOURCE_DIR = WORKING_DIR / "resources"
VIDEO_DIR = RESOURCE_DIR / "movies"
PREVIEW_DIR = RESOURCE_DIR / "previews"
THUMBNAIL_DIR = RESOURCE_DIR / "thumbnails"

# Some defaults
DEFAULT_THUMBNAIL = RESOURCE_DIR / "no-thumbnail.png"
DEFAULT_PREVIEW = RESOURCE_DIR / "no-preview.mp4"

# Typs for config.
SORT_ORDERING: ty.TypeAlias = ty.Literal["new", "old", "random", "name"]


@dt.dataclass(kw_only=True)
class Config:
    executor: ThreadPoolExecutor = dt.field(default=None)  # type: ignore
    nth_frame: ty.Optional[int] = None
    generate_thumbnails: bool = dt.field(default=False)
    generate_previews: bool = dt.field(default=False)
    sort_ordering: SORT_ORDERING = dt.field(default="name")
    retry_nonexisting: bool = False
    confirm_delete_thumbnail: bool = True
    confirm_delete_preview: bool = True
    cleanup_junk_files: bool = False
    confirm_junk_cleanup: bool = True
    defaults_size: tuple[int, int] = 512, 256
    process_statics: bool = True

    def __post_init__(self):
        if self.executor is None:
            self.executor = ThreadPoolExecutor()


def generate_thumbnails(config: Config):
    from moviepy.editor import VideoFileClip

    def save_frame(path: Path):
        image_file = THUMBNAIL_DIR / f"{path.stem}.png"
        if image_file.exists():
            return
        with VideoFileClip(str(path)) as clip:
            frame_t = (
                (clip.duration / 2) if config.nth_frame is None else config.nth_frame
            )
            clip.save_frame(str(image_file), frame_t)

    _thumbnails = lambda: filter(
        lambda path: not path.exists(),
        (THUMBNAIL_DIR / f"{video.stem}.png" for video in VIDEO_DIR.iterdir()),
    )

    wait(config.executor.submit(save_frame, video) for video in _thumbnails())

    for preview in _thumbnails():
        preview.symlink_to(DEFAULT_THUMBNAIL)


def generate_previews(config: Config):
    from mpack.previews import PreviewsSeq

    _previews = lambda: filter(
        lambda path: not path.exists(),
        (PREVIEW_DIR / video.name for video in VIDEO_DIR.iterdir()),
    )
    PreviewsSeq(video_seq=_previews(), previews_dir=PREVIEW_DIR).create()

    for preview in _previews():
        preview.symlink_to(DEFAULT_PREVIEW)


def delete_symlinks(config: Config):
    def _delete(directory: Path, default_path: Path, confirm: bool):
        paths = [
            path
            for path in directory.iterdir()
            if path.resolve().samefile(default_path)
        ]
        if confirm:
            print(f"To be deleted(symlinks): {paths}")
            value = input("Are you sure you want to continue?[y/n] ")
            if value.lower() != "y":
                return
        for path in paths:
            path.unlink()

    _delete(THUMBNAIL_DIR, DEFAULT_THUMBNAIL, config.confirm_delete_thumbnail)
    _delete(PREVIEW_DIR, DEFAULT_PREVIEW, config.confirm_delete_preview)


def cleanup_junk(config: Config):
    def _cleanup(directory: Path, todelete: ty.Callable[[Path], bool]):
        paths = [path for path in directory.iterdir() if not todelete(path)]
        if config.confirm_junk_cleanup:
            print(f"To be deleted(symlinks): {paths}")
            value = input("Are you sure you want to continue?[y/n] ")
            if value.lower() != "y":
                return
        for path in paths:
            path.unlink()

    _cleanup(THUMBNAIL_DIR, lambda p: (VIDEO_DIR / f"{p.stem}.png").exists())
    _cleanup(PREVIEW_DIR, lambda p: (VIDEO_DIR / p.name).exists())


def assert_correctness(config: Config):
    assert STATIC_DIR.exists(), f"Static directory missing: {STATIC_DIR!r}"
    assert PUBLIC_DIR.exists(), f"Public directory missing: {PUBLIC_DIR!r}"
    assert RESOURCE_DIR.exists(), f"Resources directory missing: {RESOURCE_DIR!r}"
    assert VIDEO_DIR.exists(), f"Video directory missing: {VIDEO_DIR!r}"
    assert THUMBNAIL_DIR.exists(), f"Thumbnail directory missing: {THUMBNAIL_DIR!r}"
    assert PREVIEW_DIR.exists(), f"Preview directory missing: {PREVIEW_DIR!r}"


def generate_defaults(config: Config):
    from faker import Faker

    fake = Faker()
    if not DEFAULT_THUMBNAIL.exists():
        with DEFAULT_THUMBNAIL.open("wb") as f:
            f.write(fake.image(size=config.defaults_size))
    if not DEFAULT_PREVIEW.exists():
        with tmp.TemporaryDirectory(dir="/tmp") as _dir:
            working_dir, f = Path(_dir), _DEFAULT.FRAME_FILE
            for index in range(15):
                file = working_dir / f.format(index)
                with file.open("wb") as h:
                    h.write(fake.image(size=config.defaults_size))
            Preview._image_seq_preview(working_dir, DEFAULT_PREVIEW)


def process_statics(config: Config):
    def _minify_dir(directory: Path):
        for path in directory.glob("*.min.*"):
            path.unlink()
        for file in directory.iterdir():
            process_multiple_files(str(file))
    from mpack.stream import Stream
    with Stream():
        _minify_dir(STATIC_DIR / 'js')
        _minify_dir(STATIC_DIR / 'css')


def prepare(config: Config):
    generate_defaults(config)
    if config.retry_nonexisting:
        delete_symlinks(config)
    if config.generate_thumbnails:
        generate_thumbnails(config)
    if config.generate_previews:
        generate_previews(config)
    if config.cleanup_junk_files:
        cleanup_junk(config)
    if config.process_statics:
        process_statics(config)


def get_config(app: web.Application) -> Config:
    if config := app.get(APP_KEY, None):
        return config
    raise Exception("Call setup on application to use config.")


config: ty.Callable[[web.Request], Config] = lambda req: get_config(req.app)


def setup(app: web.Application, config: ty.Optional[Config] = None):
    config = config or Config()
    assert_correctness(config)
    app[APP_KEY] = config
    prepare(config)
    return config
