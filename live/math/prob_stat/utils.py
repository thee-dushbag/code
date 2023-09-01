from random import randint
from dataclasses import dataclass, field
from statistics import mean
from math import ceil, log2, log10
import math

def random_data_x(size: int, start: int, stop: int) -> list[int]:
    assert start < stop and isinstance(start, int) and isinstance(stop, int)
    return [randint(start, stop) for _ in range(abs(size))]


def div10(number: float):
    whole, _, decimal = str(number).partition('.')
    decimal = '' if decimal == '0' else decimal
    number = int(f'{whole}{decimal}')
    decimal_places = len(decimal)
    return number, 10 ** decimal_places, decimal_places

def mrange(start: float, stop: float, step: float = 1):
    while start < stop:
        yield start
        start += step

class GroupedData:
    def __init__(self, data: list[float | int], unit_size: float = 1) -> None:
        assert len(data) > 0, "No data Available"
        self._data = sorted(data)
        self.total_freq = len(data)
        self.max_value = max(data)
        self.min_value = min(data)
        self.range = self.max_value - self.min_value
        self.number_of_classes = ceil(log2(len(data)))
        self.unit_size = unit_size
        _class_interval = self.range / self.number_of_classes
        _, _, self.unit_size_dp = div10(unit_size)
        self.class_interval = round(_class_interval, self.unit_size_dp)
        self.lower_class_limits = [*mrange(self.min_value, self.max_value + self.unit_size, self.class_interval + self.unit_size)]
        self.upper_class_limits = [lower_limit + self.class_interval for lower_limit in self.lower_class_limits]
        self.groups = [GroupClass(lower_limit, upper_limit, self.unit_size) for lower_limit, upper_limit in zip(self.lower_class_limits, self.upper_class_limits)]
        for data in self._data:
            for group in self.groups:
                group.add_item(data)
    
    def get_mean(self) -> float:
        fx = sum(g.frequency * g.mid_point for g in self.groups)
        tf = sum(g.frequency for g in self.groups)
        assert tf == self.total_freq
        return fx / self.total_freq

    def derivations_of_mean(self, mean=None):
        mean = mean or self.get_mean()
        deviation = 0
        for g in self.groups:
            deviation += (mean - g.mid_point)
        return deviation


@dataclass
class GroupClass:
    lower_class: float
    upper_class: float
    unit_size: float
    frequency: int = 0
    mid_point: float | None = None
    lower_class_boundary: int = None
    upper_class_boundary: int = None
    data: list[int] = field(default_factory=list)

    def _contains(self, other: float):
        return self.lower_class_boundary <= other <= self.upper_class_boundary

    def add_item(self, other: float | int):
        if other in self:
            self.frequency += 1
            self.data.append(other)
            return True

    def __contains__(self, other: float):
        return self._contains(other)

    def __post_init__(self):
        unit_size = 0.5 * self.unit_size
        self.mid_point = (self.upper_class + self.lower_class) / 2
        self.lower_class_boundary = self.lower_class - unit_size
        self.upper_class_boundary = self.upper_class + unit_size