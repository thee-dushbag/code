from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
import typing as ty
from xml.etree import ElementTree

import click


@dataclass
class TrackExtension:
    id: int
    application: str = "http://www.videolan.org/vlc/playlist/0"

    def tag(self) -> ElementTree.Element:
        tag = ElementTree.Element("extension", application=self.application)
        vlcid = ElementTree.SubElement(tag, f"vlc:id")
        vlcid.text = str(self.id)
        return tag


@dataclass
class Extension:
    items: ty.Sequence[int]
    application: str = "http://www.videolan.org/vlc/playlist/0"

    def tag(self) -> ElementTree.Element:
        ext = ElementTree.Element("extension", application=self.application)
        for item in self.items:
            ElementTree.SubElement(ext, "vlc:item").text = str(item)
        return ext


@dataclass
class Track:
    location: str
    title: str
    creator: str
    album: str
    trackNum: int
    extension: TrackExtension

    @property
    def duration(self) -> int:
        from moviepy.editor import AudioFileClip, VideoFileClip

        with suppress(Exception):
            return VideoFileClip(self.location).duration
        with suppress(Exception):
            return AudioFileClip(self.location).duration
        raise Exception(
            f"File is neither audio nor video: {self.location!r} or is of unknown type."
        )

    def tag(self) -> ElementTree.Element:
        from yarl import URL

        track = ElementTree.Element("track")
        ElementTree.SubElement(track, "location").text = str(URL(self.location))
        ElementTree.SubElement(track, "title").text = self.title
        ElementTree.SubElement(track, "creator").text = self.creator
        ElementTree.SubElement(track, "album").text = self.album
        ElementTree.SubElement(track, "trackNum").text = str(self.trackNum)
        ElementTree.SubElement(track, "duration").text = str(self.duration)
        track.append(self.extension.tag())
        return track

    @classmethod
    def createTrack(
        cls,
        location: str,
        trackNum: int,
        *,
        album: ty.Optional[str] = None,
        extensionID: ty.Optional[int] = None,
        creator=None,
    ) -> "Track":
        path = Path(location).absolute()
        ext = TrackExtension(extensionID or trackNum - 1)
        return cls(
            location=f"file://{path!s}",
            title=path.stem,
            creator=creator or "Unknown",
            album=album or path.parent.name,
            trackNum=trackNum,
            extension=ext,
        )


@dataclass
class PlaylistConstants:
    title: str
    trackList: list[str]
    creator: str
    album: str


@dataclass
class PlayList:
    title: str
    trackList: list[Track]

    @property
    def extension(self) -> Extension:
        items = [track.extension.id for track in self.trackList]
        return Extension(items)

    def tag(self) -> ElementTree.Element:
        attrib = {
            "xmlns": "http://xspf.org/ns/0/",
            "xmlns:vlc": "http://www.videolan.org/vlc/playlist/ns/0/",
            "version": "1",
        }
        playlist = ElementTree.Element("playlist", attrib)
        tracks = [track.tag() for track in self.trackList]
        ElementTree.SubElement(playlist, "title").text = self.title
        ElementTree.SubElement(playlist, "trackList").extend(tracks)
        playlist.append(self.extension.tag())
        return playlist

    @classmethod
    def createPlaylist(cls, const: PlaylistConstants) -> "PlayList":
        trackList = [
            Track.createTrack(track, i, album=const.album, creator=const.creator)
            for i, track in enumerate(const.trackList, start=1)
        ]
        return cls(const.title, trackList)


@click.command
@click.option(
    "--trackfile",
    "-i",
    type=click.Path(exists=True, dir_okay=False),
    help="File to get track list from.",
)
@click.option(
    "--null",
    "-0",
    help=r"Use zero terminator(\0) as a delimeter in the Piped/File input",
    is_flag=True,
)
@click.option("--album", "-a", help="Album name")
@click.option("--title", "-t", help="Title of playlist")
@click.option("--creator", "-c", help="Creator of the playlist/album/the contents.")
@click.option(
    "--output", "-o", help="File o write the playlist in, recommended extension '.xspf'"
)
def make_playlist(
    null: bool, trackfile: str, title: str, creator: str, album: str, output: str
):
    "Convert a list of paths to a vlc playlist."
    if trackfile is None:
        trackfile = input()
    else:
        trackfile = Path(trackfile).read_text()
    trackList = [line for line in trackfile.split("\0" if null else "\n") if line]
    creator = creator or "Unknown"
    album = album or "Playlist Album"
    title = title or "Playlist"
    const = PlaylistConstants(title, trackList, creator, album)
    tag = PlayList.createPlaylist(const).tag()
    ElementTree.indent(tag, "\t")
    etreestr = ElementTree.tostring(tag, encoding="utf-8", xml_declaration=True)
    if output is None:
        return click.echo(etreestr)
    path = Path(output)
    if not path.exists():
        path.touch()
    path.write_bytes(etreestr)


if __name__ == "__main__":
    make_playlist()
