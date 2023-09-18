import strawberry as straw, typing as ty, contextlib
import schema._defs as defs
from strawberry.types import Info
from strawberry.file_uploads import Upload

def _read_file(text_file: Upload) -> str:
    print(f"Text FILE: {text_file!r}")
    text_file = text_file.file  # type: ignore
    return text_file.read().decode()  # type:ignore


@straw.type
class Mutation:
    @straw.mutation
    def echo(self, string_to_echo: str) -> str:
        return string_to_echo

    @straw.mutation
    def hello(self) -> str:
        return "strawberry"

    @straw.mutation
    def set_name(self, name: str, info: Info) -> str:
        defs.NAME = name
        return name

    @straw.mutation
    def read_text(self, text_file: Upload) -> str:
        return _read_file(text_file)

    @straw.mutation
    def read_files(self, files: ty.List[Upload]) -> ty.List[str]:
        return list(map(_read_file, files))

    @straw.mutation
    def read_folder(self, folder: defs.FolderInput) -> ty.List[str]:
        return list(map(_read_file, folder.files))

    @straw.mutation
    def match_text(self, text_file: Upload, pattern: str) -> str:
        text = text_file.read().decode()  # type:ignore
        return pattern if pattern in text else ""
