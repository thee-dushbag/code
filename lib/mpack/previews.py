import concurrent.futures as cfut
from moviepy import VideoFileClip, ImageSequenceClip
from pathlib import Path
import dataclasses as dt
import tempfile as tmp
import typing as ty

NameProvider: ty.TypeAlias = ty.Callable[[Path, Path], Path]
PathLike: ty.TypeAlias = Path | str | bytes


class _DEFAULT:
    FRAMES: ty.Final[int] = 15
    FPS: ty.Final[int] = 1
    FRAME_FILE: ty.Final[str] = "{}_image.png"
    TEMPORARY_DIR: ty.Final[Path] = Path("/tmp")

    @staticmethod
    def NAME_PROVIDER(video_file: Path, output_dir: Path) -> Path:
        return output_dir / video_file.name

    @staticmethod
    def CREATE_EXECUTOR(thread_count: int | None = None):
        return cfut.ThreadPoolExecutor(thread_count)


@dt.dataclass(kw_only=True)
class Preview:
    video_file: Path
    preview_file: Path
    frames: int = dt.field(default=_DEFAULT.FRAMES)
    fps: int = dt.field(default=_DEFAULT.FPS)

    @staticmethod
    def _fixframe(frame_index: float, period: float, rounds: int = 3):
        start = frame_index * period
        fraction = period / rounds
        for i in range(rounds):
            current = i * fraction
            yield abs(start + current)
            yield abs(start - current)

    def _create_preview_frames(self, directory: Path):
        with VideoFileClip(str(self.video_file)) as vclip:
            period = round(vclip.duration / self.frames, 2)

            def _save_frame(frame_index: int):
                filename = directory / _DEFAULT.FRAME_FILE.format(frame_index)
                for frame in self._fixframe(frame_index, period):
                    try: vclip.save_frame(str(filename), frame)
                    except Exception: continue
                    else: break

            for index in range(1, self.frames + 1):
                _save_frame(index)

    @staticmethod
    def _image_seq_preview(
        images_dir: PathLike, preview_file: PathLike, fps: int = _DEFAULT.FPS
    ):
        with ImageSequenceClip(str(images_dir), fps) as iclip:
            iclip.write_videofile(str(preview_file))

    def _create_preview(self, images_dir: Path):
        self._image_seq_preview(images_dir, self.preview_file, self.fps)

    def create(self, base_dir: PathLike | None = None):
        with tmp.TemporaryDirectory(dir=str(base_dir)) as _dir:
            working_dir = Path(_dir)
            self._create_preview_frames(working_dir)
            self._create_preview(working_dir)

    async def create_async(
        self, loop=None, base_dir: PathLike | None = None, executor=None
    ):
        from asyncio import get_running_loop

        loop = loop or get_running_loop()
        return loop.run_in_executor(executor, self.create, base_dir)


@dt.dataclass(kw_only=True)
class PreviewsSeq:
    video_seq: ty.Iterable[Path]
    previews_dir: Path
    executor: cfut.Executor = dt.field(default_factory=_DEFAULT.CREATE_EXECUTOR)
    name_provider: NameProvider = dt.field(default=_DEFAULT.NAME_PROVIDER)

    def _create_preview(self, video: Path, base_dir: Path):
        preview = self.name_provider(video, self.previews_dir)
        Preview(video_file=video, preview_file=preview).create(base_dir)

    def create(self, base_dir: PathLike | None = None):
        with tmp.TemporaryDirectory(
            dir=str(base_dir or _DEFAULT.TEMPORARY_DIR)
        ) as _dir:
            working_dir = Path(_dir)
            cfut.wait(
                self.executor.submit(self._create_preview, video, working_dir)
                for video in self.video_seq
            )

    async def create_async(self, loop=None, base_dir: PathLike | None = None):
        from asyncio import get_running_loop

        loop = loop or get_running_loop()
        return loop.run_in_executor(self.executor, self.create, base_dir)


class Previews(PreviewsSeq):
    def __init__(
        self,
        *,
        video_dir: Path,
        previews_dir: Path,
        executor: cfut.Executor | None = None,
        name_provider: NameProvider | None = None,
    ):
        PreviewsSeq.__init__(
            self,
            video_seq=video_dir.iterdir(),
            previews_dir=previews_dir,
            executor=executor or _DEFAULT.CREATE_EXECUTOR(),
            name_provider=name_provider or _DEFAULT.NAME_PROVIDER,
        )
