from typing import Callable, Literal

__all__ = "Level", "Logger", "Theme", "logger", "staletheme", "State"


# LogLevels
class Level:
    NONE = 0
    DEBUG = 1 << 0
    INFO = 1 << 1
    WARN = CRITICAL = 1 << 2
    ERROR = 1 << 3
    ALL = (1 << 4) - 1


LevelType = Literal["NONE", "DEBUG", "INFO", "WARN", "CRITICAL", "ERROR", "ALL"]


# To control the log theme
class Theme:
    def __init__(
        self,
        *,
        none: str | None = None,
        text: str | None = None,
        head: str | None = None,
        info: str | None = None,
        error: str | None = None,
        debug: str | None = None,
        critical: str | None = None,
        state: str | None = None,
    ) -> None:
        self.none = "\x1b[0m" if none is None else none
        self.text = "\x1b[40;37;1m" if text is None else text
        self.state = "\x1b[40;32;1m" if state is None else state
        self.head = "\x1b[40;35;1m" if head is None else head
        self.info = "\x1b[40;34;1m" if info is None else info
        self.error = "\x1b[40;31;1m" if error is None else error
        self.debug = "\x1b[101;37;1m" if debug is None else debug
        self.critical = "\x1b[40;33;1m" if critical is None else critical


# Default Values
_DEFAULT_LOG_LEVEL = Level.ALL ^ Level.DEBUG
_DEFAULT_LOG_OUTPUT = lambda msg: print(msg, end="")
staletheme = Theme(
    info="", debug="", critical="", error="", head="", text="", none="", state=""
)


def _create_loglevel(level: LevelType):
    def log(self: "Logger", message: str, /):
        if self.levelon(getattr(Level, level)):
            self._log_message(level, message)

    return log


class State:
    def __init__(self, logger: "Logger", state: str) -> None:
        self._logger = logger
        self._state = state

    @property
    def state(self) -> str:
        return self._state

    def __enter__(self):
        self._logger._states.append(self)
        return self._logger

    def __exit__(self, etype, eval, etb):
        self._logger._states.remove(self)


# The logger itself
class Logger:
    def __init__(
        self,
        name: str | None = None,
        *,
        log_level: int | None = None,
        theme: Theme | None = None,
        writer: Callable[[str], object] | None = None,
        show_state=None,
    ):
        self._name = name
        self.theme = theme or staletheme
        self.writer = writer or _DEFAULT_LOG_OUTPUT
        self.level = _DEFAULT_LOG_LEVEL if log_level is None else log_level
        self._states: list[State] = []
        self.show_state = show_state or True

    @property
    def name(self) -> str | None:
        return self._name

    def _log_message(self, level: str, msg: str):
        data: list[str] = []
        t = self.theme
        if self._name is not None:
            data.append(f"{t.head}{self._name}")
        data.append(f"{getattr(t, level.lower())}{level.upper()}")
        if self._states and self.show_state:
            data.append(
                f"{t.text}{'{'}"
                + f"{t.head},".join(f"{t.state}{w.state}" for w in self._states)
                + f"{t.text}{'}'}"
            )
        data.append(f" {msg}{t.none}\n")
        self.writer(f"{t.text}:".join(data))

    def turnon(self, level: int):
        self.level |= level

    def turnoff(self, level: int):
        self.level ^= self.level & level

    def levelon(self, level: int) -> bool:
        return self.level & level == level

    def leveloff(self, level: int) -> bool:
        return self.level & level == 0

    def state(self, state: str):
        return State(self, state)

    def mute(self) -> int:
        level = self.level
        self.level = Level.NONE
        return level

    def unmute(self, level: int | None = None, /):
        self.level = Level.ALL if level is None else level

    error = _create_loglevel("ERROR")
    info = _create_loglevel("INFO")
    warn = critical = _create_loglevel("CRITICAL")
    debug = _create_loglevel("DEBUG")
    _loggers = {error, info, warn, debug}


# Default logger
logger = Logger("ROOT", log_level=Level.ALL, theme=Theme())
