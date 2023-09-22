from random import randint
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from bivariate_data import (linear_regression, pearsons_product_correlation_r1,
                            pearsons_product_correlation_r2,
                            spearman_rank_correlation)

weight = 78, 86, 72, 82, 80, 86, 84, 89, 68, 71
blood_pressure = 140, 160, 134, 144, 180, 176, 174, 178, 128, 132

mean_temp = 14.2, 14.3, 14.6, 14.9, 15.2, 15.6, 15.9
pirates = 35000, 45000, 20000, 15000, 5000, 400, 17

sqrs_x = tuple(range(1, 10))
sqrs_y = tuple(sorted((10 * x + 50 for x in sqrs_x)))

SIZE = 20
rand_x = tuple(randint(0, 1000) for _ in range(SIZE))
rand_y = tuple(randint(5000, 6000) for _ in range(SIZE))

grd_pnt_avg = 8.3, 8.6, 9.2, 9.8, 8.0, 7.8, 9.4, 9.0, 7.2, 8.6
exm_scr = 2300, 2250, 2380, 2400, 2000, 2100, 2360, 2350, 2000, 2260
xs, ys = mean_temp, pirates
xs, ys = grd_pnt_avg, exm_scr
xs, ys = weight, blood_pressure
xs, ys = rand_x, rand_y
xs, ys = sqrs_x, sqrs_y
xlabel, ylabel = "Weight", "Blood Pressure"
xlabel, ylabel = "x", "y"
xlabel, ylabel = "Random X value", "Random Y Value"
xlabel, ylabel = "x", "Sqr(x)"


def compute_correlation_s(lxs, lys):
    plt.scatter(xs, ys)
    plt.scatter(lxs, lys)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    correlation_1 = pearsons_product_correlation_r1(xs, ys)
    correlation_2 = pearsons_product_correlation_r2(xs, ys)
    correlation_3 = spearman_rank_correlation(xs, ys)
    print(f"The Predictor Chance of Correctness: {round(abs(correlation_3) * 100, 2)}%")
    print(f"Correlation_1 Coefficient: {correlation_1}")
    print(f"Correlation_2 Coefficient: {correlation_2}")
    print(f"Correlation_3 Coefficient: {correlation_3}")
    c1 = round(correlation_1, 2)
    c2 = round(correlation_2, 2)
    c3 = round(correlation_3, 2)
    plt.title(f"Correlation: {c1=} {c2=} {c3=}")
    plt.show()


def main(argv: Sequence[str]) -> None:
    # for i in range(10):
    start = min(xs) - 10
    stop = max(xs) + 10
    xs_tests = np.arange(start, stop, 1)
    y_pred = linear_regression(xs, ys, xlabel)
    print(f"Predicter: {y_pred.str}")
    ys_pred = tuple(map(y_pred, xs_tests))
    compute_correlation_s(xs_tests, ys_pred)


if __name__ == "__main__":
    from sys import argv

    main(argv[1:])
