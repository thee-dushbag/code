from pathlib import Path
from faker import Faker
from mpack.preview import TemporaryDir, Preview

FAKE = Faker()
WORKING_DIR = Path.cwd()
CONTENT_DIR = Path.home() / 'Content'
RESOURCE_DIR = CONTENT_DIR / '.bin' / 'resources'
MOVIEAPP_DIR = RESOURCE_DIR / 'movie-app'

MOVIE_DIR = MOVIEAPP_DIR / 'movies'
THUMBNAIL_DIR = MOVIEAPP_DIR / 'thumbnails'
PREVIEW_DIR = MOVIEAPP_DIR / 'previews'
NO_THUMBNAIL = THUMBNAIL_DIR / 'no-thumbnail.png'
NO_PREVIEW = PREVIEW_DIR / 'no-preview.mp4'

STATIC_DIR = WORKING_DIR / 'static'
TEMPLATES_DIR = WORKING_DIR / 'templates'

if not NO_THUMBNAIL.exists():
    NO_THUMBNAIL.touch()
    NO_THUMBNAIL.write_bytes(FAKE.image(size=(512, 256)))

if not NO_PREVIEW.exists():
    with TemporaryDir() as dir:
        for i in range(15):
            imagename = dir / f'image_{i}.png'
            imagename.write_bytes(FAKE.image(size=(512, 256)))
        Preview(NO_PREVIEW, dir).create()