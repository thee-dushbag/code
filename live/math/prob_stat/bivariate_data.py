from dataclasses import dataclass, field
from itertools import tee
from math import sqrt
from statistics import mean
from typing import Sequence, cast

from more_itertools import bucket

_prod = lambda i, j: i * j


def _minus_this(constant: float):
    def inner(variable: float):
        return variable - constant

    return inner


def pearsons_product_correlation_r1(x: Sequence[float], y: Sequence[float]) -> float:
    assert (freq := len(x)) == len(y), "xs must be pairable to ys"
    xm, ym = mean(x), mean(y)
    _xm, _ym = _minus_this(xm), _minus_this(ym)
    d_prod = lambda _x, _y: _prod(_xm(_x), _ym(_y))
    num = sum(map(d_prod, x, y))
    sum_x_xm = sum(map(_prod, *tee(map(_xm, x))))
    sum_y_ym = sum(map(_prod, *tee(map(_ym, y))))
    den = sqrt(sum_x_xm * sum_y_ym)
    return num / den


def pearsons_product_correlation_r2(x: Sequence[float], y: Sequence[float]) -> float:
    assert (freq := len(x)) == len(y), "xs must be pairable to ys"
    sum_x, sum_y = sum(x), sum(y)
    sum_xy = sum(map(_prod, x, y))
    sum_xx = sum(map(_prod, x, x))
    sum_yy = sum(map(_prod, y, y))
    num = freq * sum_xy - sum_x * sum_y
    pden1 = freq * sum_xx - sum_x**2
    pden2 = freq * sum_yy - sum_y**2
    den = sqrt(pden1 * pden2)
    return num / den


@dataclass
class Rank:
    value: float
    ranks: Sequence[float]
    rank: float | None = None

    def __post_init__(self):
        if not self.ranks:
            self.ranks = (0,)
        self.rank = mean(self.ranks)


def _rank_classifier(rank_val: tuple[float, float]):
    return rank_val[1]


@dataclass
class Values:
    values: Sequence[float]
    ranks: Sequence[float] = field(default=tuple())
    cranks: Sequence[Rank] = field(default=tuple())

    def __post_init__(self):
        self.values = tuple(sorted(self.values))
        if self.ranks == tuple():
            _e = len(self.values) + 1
            ranks = reversed(range(1, _e))
            self.ranks = tuple(ranks)
        rank_val = zip(self.ranks, self.values)
        cranks = bucket(rank_val, key=_rank_classifier)
        ranks_table: dict[float, list] = {}
        cranks_ = []
        for value in self.values:
            if value in ranks_table:
                ranks = ranks_table[value]
            else:
                ranks = list(_rnk[0] for _rnk in cranks[value])
                ranks_table[value] = ranks
            crank = Rank(value, ranks)
            cranks_.append(crank)
        self.cranks = tuple(cranks_)

    def getvaluerank(self) -> dict[float, float]:
        return {rank.value: cast(float, rank.rank) for rank in self.cranks}


def spearman_rank_correlation(x: Sequence[float], y: Sequence[float]):
    assert (freq := len(x)) == len(y), "xs must be pairable to ys"
    x_values, y_values = Values(x), Values(y)
    x_vranks, y_vranks = x_values.getvaluerank(), y_values.getvaluerank()
    paired_ranks = tuple((x_vranks[xv], y_vranks[yv]) for xv, yv in zip(x, y))
    differences = tuple(i - j for i, j in paired_ranks)
    sqr_differences = map(lambda x: x**2, differences)
    sum_sqr_diff = sum(sqr_differences)
    den, num = freq * (freq**2 - 1), 6 * sum_sqr_diff
    return 1 - (num / den)


def _linear_regression_predicter(a: float, b: float, xstr=None):
    xstr = str(xstr or "").replace(" ", "_").lower() or "x"

    def predict(x: float):
        return a + b * x

    ra, rb = round(a, 3), round(b, 3)
    predict.str = f"predict({rb} * {xstr} + {ra})"
    return predict


def _linear_regression_compute_a(b: float, x: Sequence[float], y: Sequence[float]):
    assert (freq := len(x)) == len(y), "xs must be pairable to ys"
    sum_x, sum_y = sum(x), sum(y)
    num = sum_y - b * sum_x
    return num / freq


def _linear_regression_compute_b(x: Sequence[float], y: Sequence[float]):
    assert (freq := len(x)) == len(y), "xs must be pairable to ys"
    sum_xy = sum(map(_prod, x, y))
    sum_x, sum_y = sum(x), sum(y)
    sum_xx = sum(map(_prod, x, x))
    num = freq * sum_xy - sum_x * sum_y
    den = freq * sum_xx - sum_x**2
    return num / den


def linear_regression(x: Sequence[float], y: Sequence[float], xstr=None):
    b = _linear_regression_compute_b(x, y)
    a = _linear_regression_compute_a(b, x, y)
    return _linear_regression_predicter(a, b, xstr)
