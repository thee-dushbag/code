import enum
from typing import Any, Protocol, SupportsFloat, TypeGuard

from attrs import asdict, define, field

MILLISEONDS_SECONDS = 0.001
SECONDS_MILLISECONDS = 1000
SECOND_SECONDS = 1
MINUTE_SECONDS = 60
HOUR_SECONDS = 3600
DAY_SECONDS = HOUR_SECONDS * 24
WEEK_SECONDS = DAY_SECONDS * 7
PRETTY_TIME_FORMAT = (
    "%(hours)dhours %(minutes)dminutes %(seconds)d.%(milliseconds)dseconds in %(state)s"
)


class Timable(Protocol):
    def __time_seconds__(self) -> float:
        ...


def _is_timable(time: Any) -> TypeGuard[Timable]:
    return hasattr(time, "__time_seconds__")


SupportsTimable = Timable | SupportsFloat


def timable(time: SupportsTimable) -> float:
    if _is_timable(time):
        return time.__time_seconds__()
    return float(time)  # type:ignore


def pretty_time(time: SupportsTimable) -> str:
    t = Time(timable(time))
    return PRETTY_TIME_FORMAT % asdict(t)


def to_hours(time: SupportsTimable) -> float:
    return timable(time) / HOUR_SECONDS


def to_minutes(time: SupportsTimable) -> float:
    return timable(time) / MINUTE_SECONDS


def to_days(time: SupportsTimable) -> float:
    return timable(time) / DAY_SECONDS


def to_weeks(time: SupportsTimable) -> float:
    return timable(time) / WEEK_SECONDS


def to_seconds(time: SupportsTimable) -> float:
    return timable(time) / SECOND_SECONDS


def to_milliseconds(time: SupportsTimable) -> float:
    return timable(time) / MILLISEONDS_SECONDS


def hours_to_days(time: float):
    secs = time * HOUR_SECONDS
    return to_days(secs)


@define(slots=True)
class Time:
    class TimeState(enum.StrEnum):
        FUTURE = enum.auto()
        PAST = enum.auto()

    _time: float = field(factory=float, converter=float, eq=False, repr=False)
    hours: int = field(factory=int, converter=int, kw_only=True)
    minutes: int = field(factory=int, converter=int, kw_only=True)
    seconds: int = field(factory=int, converter=int, kw_only=True)
    milliseconds: int = field(factory=int, converter=int, kw_only=True)
    state: TimeState = field(default=TimeState.FUTURE, init=False)

    def __time_seconds__(self):
        return self.time

    def __attrs_post_init__(self):
        self._set_state()
        tmp_time = abs(self._time)
        hours, tmp_time = divmod(tmp_time, 3600)
        minutes, tmp_time = divmod(tmp_time, 60)
        seconds, tmp_time = divmod(tmp_time, 1)
        milliseconds = round(tmp_time * 1000, 3)
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.seconds = int(seconds)
        self.milliseconds = int(milliseconds)

    def _set_state(self):
        secs = self.seconds
        hrs = self.hours * 3600
        mins = self.minutes * 60
        mils = self.milliseconds / 1000
        self._time += hrs + secs + mins + mils
        if self._time < 0:
            self.state = Time.TimeState.PAST

    def __add__(self, time: "Time") -> "Time":
        return Time(self.time + time.time)

    def __sub__(self, time: "Time") -> "Time":
        return Time(self.time - time.time)

    def _get_time(self):
        hrs, mins = self.hours * 3600, self.minutes * 60
        secs, mls = self.seconds * 1, self.milliseconds / 1000
        return hrs + mins + secs + mls

    @property
    def time(self) -> float:
        _t: float = self._get_time()
        if self.state == Time.TimeState.PAST:
            _t = 0 - _t
        return _t


@define(slots=True)
class WeekTime(Time):
    days: int = field(factory=int, converter=int, kw_only=True)
    weeks: int = field(factory=int, converter=int, kw_only=True)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        days, self.hours = divmod(self.hours, 24)
        weeks, days = divmod(days, 7)
        self.days = int(days)
        self.weeks = int(weeks)

    def _set_state(self):
        self.days += self.weeks * 7
        self.hours += self.days * 24
        super()._set_state()

    def _get_time(self):
        return (self.days + self.weeks * 7) * 24 * 3600 + super()._get_time()
