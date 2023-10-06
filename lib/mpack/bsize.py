import dataclasses as dt
import enum as _e
import typing as ty
from copy import copy
from warnings import warn as _warn

# Exports...
__all__ = (
    # Size class
    "Bytes",
    # Constants
    "Size",
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


# Constants
class Size(_e.IntEnum):
    """Class represents the size constants: bytes, bits, ..."""

    # kept 8 because of consistensy, this is an int enum after all...(*_*)
    BITS = 1 << 3  # 8 (8bits = 1byte)
    BYTES = 1 << 0  # 1 (base constant)
    KILO_BYTES = BYTES << 10  # 1024
    MEGA_BYTES = BYTES << 20  # 1024 * 1024
    GIGA_BYTES = BYTES << 30  # 1024 * 1024 * 1024
    TERRA_BYTES = BYTES << 40  # 1024 * 1024 * 1024 * 1024
    PETA_BYTES = BYTES << 50  # 1024 * 1024 * 1024 * 1024 * 1024


# Legacy Constants: Keep for the memories...
# TODO: Place these constants in an enum...(*_*)   **DONE**
# BYTES = 1
# BITS = BYTES * 8
# KILO_BYTES = 1024 * BYTES
# MEGA_BYTES = 1024 * KILO_BYTES
# GIGA_BYTES = 1024 * MEGA_BYTES
# TERRA_BYTES = 1024 * GIGA_BYTES
# PETA_BYTES = 1024 * TERRA_BYTES


# Converters
## From * to bytes...
def b_bytes(b: ty.SupportsFloat) -> float:
    return float(b) / Size.BITS


def kb_bytes(kb: ty.SupportsFloat) -> float:
    return float(kb) * Size.KILO_BYTES


def mb_bytes(mb: ty.SupportsFloat) -> float:
    return float(mb) * Size.MEGA_BYTES


def gb_bytes(gb: ty.SupportsFloat) -> float:
    return float(gb) * Size.GIGA_BYTES


def tb_bytes(tb: ty.SupportsFloat) -> float:
    return float(tb) * Size.TERRA_BYTES


def pb_bytes(pb: ty.SupportsFloat) -> float:
    return float(pb) * Size.PETA_BYTES


## From bytes to *...
def bytes_b(by: ty.SupportsFloat) -> float:
    return float(by) * Size.BITS


def bytes_kb(by: ty.SupportsFloat) -> float:
    return float(by) / Size.KILO_BYTES


def bytes_mb(by: ty.SupportsFloat) -> float:
    return float(by) / Size.MEGA_BYTES


def bytes_gb(by: ty.SupportsFloat) -> float:
    return float(by) / Size.GIGA_BYTES


def bytes_tb(by: ty.SupportsFloat) -> float:
    return float(by) / Size.TERRA_BYTES


def bytes_pb(by: ty.SupportsFloat) -> float:
    return float(by) / Size.PETA_BYTES


# Base Class For representing size...
# TODO: It's cliche to name it 'Bytes'. Give better name...
# TODO: Use properties instead of instance variables to replace Bytes.align
# FATAL: Using properties means to stop using dataclass...(-_-)
@dt.dataclass(slots=True)
class Bytes:
    """Class Represents size"""

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
        self.peta_bytes, size = divmod(size, Size.PETA_BYTES)
        self.terra_bytes, size = divmod(size, Size.TERRA_BYTES)
        self.giga_bytes, size = divmod(size, Size.GIGA_BYTES)
        self.mega_bytes, size = divmod(size, Size.MEGA_BYTES)
        self.kilo_bytes, size = divmod(size, Size.KILO_BYTES)
        self.bytes, size = divmod(size, Size.BYTES)
        self.bits = int(size * Size.BITS)

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
# This is a very poor, weak and naive implementation
# of a formatter of its kind.
# TODO: Research better ways to implement this.
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


# For backward compatibility with legacy code...
_SIZES = [
    "BYTES",
    "BITS",
    "KILO_BYTES",
    "MEGA_BYTES",
    "GIGA_BYTES",
    "TERRA_BYTES",
    "PETA_BYTES",
]


# issue warning on old usage in favor for latest syntax and design...
def __getattr__(name: str, default: ty.Any = None):
    if name in _SIZES:
        _warn(
            f"Use Enum class 'Size' to access the size constants including: {name!r} as 'Size.{name}'",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return getattr(Size, name, default)
    raise AttributeError(f"Attribute {name!r} not found in Module {__name__!r}")
