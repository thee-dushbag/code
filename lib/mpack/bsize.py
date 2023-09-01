import typing as ty, dataclasses as dt
from copy import copy

# Constants
# TODO: Place these constants in an enum...(*_*)
BYTES = 1
BITS = BYTES * 8
KILO_BYTES = 1024 * BYTES
MEGA_BYTES = 1024 * KILO_BYTES
GIGA_BYTES = 1024 * MEGA_BYTES
TERRA_BYTES = 1024 * GIGA_BYTES
PETA_BYTES = 1024 * TERRA_BYTES


# Converters
## From * to bytes...
def b_bytes(b: int) -> float: return b / BITS
def kb_bytes(kb: float) -> float: return kb * KILO_BYTES
def mb_bytes(mb: float) -> float: return mb * MEGA_BYTES
def gb_bytes(gb: float) -> float: return gb * GIGA_BYTES
def tb_bytes(tb: float) -> float: return tb * TERRA_BYTES
def pb_bytes(pb: float) -> float: return pb * PETA_BYTES

## From bytes to *...
def bytes_b(by: int) -> float: return by * BITS
def bytes_kb(by: float) -> float: return by / KILO_BYTES
def bytes_mb(by: float) -> float: return by / MEGA_BYTES
def bytes_gb(by: float) -> float: return by / GIGA_BYTES
def bytes_tb(by: float) -> float: return by / TERRA_BYTES
def bytes_pb(by: float) -> float: return by / PETA_BYTES


# Base Class For representing size...
# TODO: It's cliche to name it 'Bytes'. Give better name...
# TODO: Use properties instead of instance variables to replace Bytes.align
# FATAL: Using properties means to stop using dataclass...(-_-)
@dt.dataclass(slots=True)
class Bytes:
    bytes: float = dt.field(default=0)
    bits: int = dt.field(default=0, kw_only=True)
    kilo_bytes: float = dt.field(default=0, kw_only=True)
    mega_bytes: float = dt.field(default=0, kw_only=True)
    giga_bytes: float = dt.field(default=0, kw_only=True)
    terra_bytes: float = dt.field(default=0, kw_only=True)
    peta_bytes: float = dt.field(default=0, kw_only=True)

    def __post_init__(self):
        self.align()

    def assign(self, size: float):
        self._assign(abs(size))
        return self

    def align(self):
        raw_size = self._to_bytes()
        return self.assign(raw_size)

    def _to_bytes(self) -> float:
        return sum(
            (
                self.bytes,
                pb_bytes(self.peta_bytes),
                tb_bytes(self.terra_bytes),
                gb_bytes(self.giga_bytes),
                mb_bytes(self.mega_bytes),
                kb_bytes(self.kilo_bytes),
                b_bytes(self.bits),
            )
        )

    def _assign(self, size: float):
        self.peta_bytes, size = divmod(size, PETA_BYTES)
        self.terra_bytes, size = divmod(size, TERRA_BYTES)
        self.giga_bytes, size = divmod(size, GIGA_BYTES)
        self.mega_bytes, size = divmod(size, MEGA_BYTES)
        self.kilo_bytes, size = divmod(size, KILO_BYTES)
        self.bytes, size = divmod(size, BYTES)
        self.bits = int(size * BITS)

    def __float__(self) -> float:
        return self._to_bytes()

    def __add__(self, other: ty.SupportsFloat) -> ty.Self:
        return self.__class__(float(other) + float(self))

    def __sub__(self, other: ty.SupportsFloat) -> ty.Self:
        return self.__class__(float(other) - float(self))

    def __mul__(self, other: ty.SupportsFloat) -> ty.Self:
        return self.__class__(float(other) * float(self))

    def __div__(self, other: ty.SupportsFloat) -> ty.Self:
        return self.__class__(float(self) / float(other))

    def __format__(self, format_spec: str) -> str:
        return _Formatter.format(self, format_spec)


def _converter(format_spec: str):
    def _abbr(abbr: str) -> ty.Callable[[float], float]:
        fmt = format_spec.format(abbr=abbr)
        return globals().get(fmt, float)

    return _abbr


# Helper formatter for the Size(aka Bytes) class...
class _Formatter:
    _bx = _converter("bytes_{abbr}")
    _xb = _converter("{abbr}_bytes")

    patterns = dict(
        bytes=("%b", _xb("bytes")),
        kilo_bytes=("%k", _xb("kb")),
        mega_bytes=("%m", _xb("mb")),
        giga_bytes=("%g", _xb("gb")),
        terra_bytes=("%t", _xb("tb")),
        peta_bytes=("%p", _xb("pb")),
    )

    absolute_patterns = dict(
        bytes=("%B", _bx("bytes")),
        kilo_bytes=("%K", _bx("kb")),
        mega_bytes=("%M", _bx("mb")),
        giga_bytes=("%G", _bx("gb")),
        terra_bytes=("%T", _bx("tb")),
        peta_bytes=("%P", _bx("pb")),
    )

    @classmethod
    def _abs_format(cls, bytes: Bytes, format_spec: str):
        b = float(bytes)
        for _, (string, conv) in cls.absolute_patterns.items():
            format_spec = format_spec.replace(string, str(conv(b)))
        return format_spec

    @classmethod
    def _format(cls, b: Bytes, format_spec: str):
        for key, (string, _) in cls.patterns.items():
            repl = str(int(getattr(b, key, 0)))
            format_spec = format_spec.replace(string, repl)
        return format_spec

    @classmethod
    def format(cls, bytes: Bytes, format_spec: str) -> str:
        b = copy(bytes).align()
        format_spec = cls._abs_format(b, format_spec)
        return cls._format(b, format_spec)


# Exports...
__all__ = (
# Size class
    "Bytes",
# Constants
    "BYTES",
    "BITS",
    "KILO_BYTES",
    "MEGA_BYTES",
    "GIGA_BYTES",
    "TERRA_BYTES",
    "PETA_BYTES",
# Converters
    "b_bytes",
    "kb_bytes",
    "mb_bytes",
    "gb_bytes",
    "tb_bytes",
    "pb_bytes",
    "bytes_b",
    "bytes_kb",
    "bytes_mb",
    "bytes_gb",
    "bytes_tb",
    "bytes_pb",
)
