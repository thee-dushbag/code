from statistics import mean, median, geometric_mean, harmonic_mean
from utils import random_data_x
from math import ceil, floor
from typing import Sequence
from functools import reduce
from rich.console import Console
console = Console()
print = console.print

def m_mean(data: list[int]):
    freq = len(data)
    return sum(data) / freq

def m_harmonic_mean(data: list[int]):
    den = sum(1 / d for d in data)
    return len(data) / den

def m_median(data: list[int]):
    freq = len(data)
    data = sorted(data)
    _v = (freq + 1) / 2
    points = (ceil(_v), floor(_v)) if freq % 2 == 0 else (floor(_v),)
    vals = [data[p - 1] for p in points]
    return sum(vals) / len(vals)

def m_geometric_mean(data: list[int]):
    prod = reduce(lambda x, y: x * y, data)
    return pow(prod, 1 / len(data))

def main(argv: Sequence[str]) -> None:
    # data = [*range(1, 50, 3)]
    data = random_data_x(21, 50, 250)
    m_mean_ = m_mean(data)
    mean_ = mean(data)
    median_ = median(data)
    m_median_ = m_median(data)
    gmean = geometric_mean(data)
    m_gmean = m_geometric_mean(data)
    hmean = harmonic_mean(data)
    m_hmean = m_harmonic_mean(data)
    deviations = sum(x - mean_ for x in data)
    print(f"Data: {data}")
    print(f"s_Data: {sorted(data)}")
    print(f"Mean: {mean_}")
    print(f"m_Mean: {m_mean_}")
    print(f"GeometricMean: {gmean}")
    print(f"m_GeometricMean: {m_gmean}")
    print(f"HarmonicMean: {hmean}")
    print(f"m_HarmonicMean: {m_hmean}")
    print(f"Median: {median_}")
    print(f"m_Median: {m_median_}")
    print(f"Deviation: {deviations}")



if __name__ == '__main__':
    from sys import argv
    main(argv[1:])