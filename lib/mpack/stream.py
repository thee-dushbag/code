import sys, typing as ty, dataclasses as dt

__all__ = (
    "reset",
    "redirect",
    "StreamFiles",
    "Stream",
    "get_null_stream",
    "set_null_stream",
    "get_original_stream",
    "get_current_stream",
    "create_null_stream",
)


@dt.dataclass
class StreamFiles:
    errfile: ty.TextIO
    outfile: ty.TextIO
    infile: ty.TextIO

    @classmethod
    def create(cls, *, current=None, errfile=None, outfile=None, infile=None):
        current = current or get_current_stream()
        if errfile is None:
            errfile = current.errfile
        if outfile is None:
            outfile = current.outfile
        if infile is None:
            infile = current.infile
        return cls(errfile=errfile, outfile=outfile, infile=infile)

    @classmethod
    def _same_stream(cls, file: "StreamFiles", other: "StreamFiles") -> bool:
        "Simply compares the file descriptors of the file streams."
        return all(
            (
                file.errfile.fileno() == other.errfile.fileno(),
                file.infile.fileno() == other.infile.fileno(),
                file.outfile.fileno() == other.outfile.fileno(),
            )
        )

    def __eq__(self, __value: "StreamFiles") -> bool:
        if not isinstance(__value, self.__class__):
            raise TypeError(f"Expected a StreamFiles object, found: {type(__value)}")
        return self._same_stream(self, __value)

    def __init_subclass__(cls) -> None:
        raise Exception("Do not subclass this class.")


def create_null_stream(nullfile: str, *, own=False):
    oefile = open(nullfile, "w")
    ifile = open(nullfile, "r")

    if not own:
        from atexit import register
        @register
        def _close_nullfile():
            if not oefile.closed:
                oefile.close()
            if not ifile.closed:
                ifile.close()

    return StreamFiles(errfile=oefile, outfile=oefile, infile=ifile)


def get_current_stream() -> StreamFiles:
    return StreamFiles(outfile=sys.stdout, errfile=sys.stderr, infile=sys.stdin)


# Ensure Backing up the core stream files
# Supposedly: Provided this module was not
# imported before sys._stream_files were changed
_original_sys_files: StreamFiles = get_current_stream()

# For *my* system Blackhole file: Probably all linux os.
# TODO: Use match or if blocks to set correct
#       Null file target depending on the host
#       Operating System. (*_*)
_null_system_file: str = "/dev/null"
# Dont mind this. Will be set later when needed.
_null_stream: StreamFiles = None  # type: ignore


def _null_stream_handler(null_stream: ty.Optional[StreamFiles] = None) -> StreamFiles:
    global _null_stream
    if null_stream is not None:
        _null_stream = null_stream  # Told Yeah
    if _null_stream is None:
        _null_stream = create_null_stream(_null_system_file)  # Told Yeah
    return _null_stream


def get_null_stream() -> StreamFiles:
    "Get the system black hole stream."
    return _null_stream_handler()


def set_null_stream(stream: StreamFiles):
    "Set blackhole stream for the system. A stream that consumes all and reads empty strings"
    _null_stream_handler(stream)


def set_original_stream(stream: StreamFiles):
    "Set a stream as the original system streams."
    global _original_sys_files
    _original_sys_files = stream


def get_original_stream():
    "Get original system python streams."
    return _original_sys_files


def _redirect_to(files: StreamFiles):
    sys.stderr = files.errfile
    sys.stdout = files.outfile
    sys.stdin = files.infile


def _reset_streams():
    _redirect_to(_original_sys_files)


def redirect(stream: ty.Optional[StreamFiles] = None):
    "Set the current stream to :stream: or :null_stream: if stream is None."
    if stream is None:
        stream = _null_stream
    _redirect_to(stream)


def reset():
    "Set the original streams back as current streams"
    _reset_streams()


@dt.dataclass
class Stream:
    stream: StreamFiles = dt.field(default_factory=get_null_stream)
    error_stream: ty.Optional[ty.TextIO] = dt.field(default=None, kw_only=True)
    out_stream: ty.Optional[ty.TextIO] = dt.field(default=None, kw_only=True)
    in_stream: ty.Optional[ty.TextIO] = dt.field(default=None, kw_only=True)
    _ostream: StreamFiles = dt.field(init=False, default_factory=get_null_stream)
    _streaming: bool = dt.field(init=False, default=False)

    def __post_init__(self):
        self.stream = StreamFiles.create(
            current=self.stream,
            errfile=self.error_stream,
            outfile=self.out_stream,
            infile=self.in_stream,
        )

    def start(self):
        if self._streaming:
            return
        self._ostream = get_current_stream()
        redirect(self.stream)
        self._streaming = True

    def stop(self):
        if not self._streaming:
            return
        redirect(self._ostream)
        self._streaming = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()
