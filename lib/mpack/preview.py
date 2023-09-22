import asyncio as aio
import shutil as shu
from pathlib import Path
from random import choices
from string import ascii_lowercase, digits

import attrs
from moviepy.editor import ImageSequenceClip, VideoFileClip


@attrs.define
class Preview:
    preview_filename: Path
    images_dir: Path
    fps: int = attrs.field(default=1, kw_only=True)

    def _create_preview(self):
        with ImageSequenceClip(str(self.images_dir), self.fps) as clip:
            clip.write_videofile(str(self.preview_filename), threads=3)

    def create(self):
        return self._create_preview()


def _create_tmp_dir(parent: Path, c=0) -> Path:
    if c >= 50:
        raise OSError("Unable to create a random file name.")
    envname = "".join(choices(ascii_lowercase + digits, k=10 + c))
    dir, c = parent / f"TMP_{envname}", c + 1
    return dir if not dir.exists() else _create_tmp_dir(parent, c)


def _make_dir(parent: Path):
    return parent if parent.is_dir() else parent.parent


@attrs.define
class TemporaryDir:
    parent: Path = attrs.field(factory=Path.cwd, converter=_make_dir)
    dir: Path = attrs.field(init=False, default=None)

    def __attrs_post_init__(self):
        self.dir = _create_tmp_dir(self.parent)

    def __enter__(self):
        print(f"Creating Temporary Directory: {str(self.dir)}")
        if not self.dir.exists():
            self.dir.mkdir()
        assert self.dir.is_dir()
        return self.dir

    def __exit__(self, *_, **__):
        print(f"Deleting Temporary Directory: {str(self.dir)}")
        shu.rmtree(self.dir)


@attrs.define
class PreviewEnv:
    clip: Path
    env_dir: Path
    preview_dir: Path = attrs.field(default=None)
    preview_name: Path = attrs.field(default=None)
    image_count: int = attrs.field(default=15)

    def __attrs_post_init__(self):
        if self.clip.parent == self.preview_dir:
            self.preview_dir = None
        if self.preview_name is None:
            if self.preview_dir is None:
                preview_name = self.clip.stem + "_preview"
                p = self.clip.with_stem(preview_name)
            else:
                p = self.preview_dir / self.clip.name
        else:
            self.preview_name = (
                str(self.preview_name)
                if not type(self.preview_name) == Path
                else self.preview_name
            )
            if self.preview_dir is None:
                p = self.clip.parent / self.preview_name
            else:
                p = self.preview_dir / self.preview_name
        self.preview_name = p

    def _prepare_env(self):
        with TemporaryDir(self.env_dir) as dir:
            self._save_frames(dir)
            self._create_preview(dir)

    def _save_frames(self, image_dir):
        video = VideoFileClip(str(self.clip))
        image_count = (
            video.duration if video.duration <= self.image_count else self.image_count
        )
        period = int(video.duration / image_count)
        for i in range(1, image_count + 1):
            imagefile = image_dir / f"image_{i}.png"
            video.save_frame(str(imagefile), i * period)
        video.close()

    def _create_preview(self, image_dir):
        Preview(self.preview_name, image_dir).create()

    def create(self):
        self._prepare_env()

    async def create_async(self):
        loop = aio.get_running_loop()
        await loop.run_in_executor(None, self.create)


@attrs.define
class Previews:
    clips: list[Path] = attrs.field(converter=list)
    previews_dir: Path = attrs.field(default=None)

    def __attrs_post_init__(self):
        if self.previews_dir is None:
            if self.clips:
                self.previews_dir = self.clips[0].parent

    def create(self, tmp_dir=None):
        tmp = tmp_dir or Path.cwd()
        with TemporaryDir(tmp) as dir:
            for clip in self.clips:
                PreviewEnv(clip, dir, self.previews_dir).create()

    def _previewenv(self, clip: Path, dir: Path, img_cnt=15):
        return PreviewEnv(
            clip, dir, self.previews_dir, image_count=img_cnt
        ).create_async()

    def _previewenvs(self, dir, clips: list[Path], img_cnt=15):
        return (self._previewenv(c, dir, img_cnt) for c in clips)

    async def create_async(self, tmp_dir=None, img_cnt=15):
        tmp = tmp_dir or Path.cwd()
        with TemporaryDir(tmp) as dir:
            tasks = self._previewenvs(dir, self.clips, img_cnt)
            return await aio.gather(*tasks, return_exceptions=True)
