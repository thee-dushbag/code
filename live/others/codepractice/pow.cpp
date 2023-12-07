#include <iostream>
#include <unordered_map>
#include <cmath>
#include <iomanip>
#include <vector>
#include <span>
#include <limits>
#include "helpers.hpp"

/*
Implement pow(x, n), which calculates x
raised to the power n (i.e., x^n).

Example 1:

Input: x = 2.00000, n = 10
Output: 1024.00000

Example 2:
  Input: x = 2.10000, n = 3
  Output: 9.26100

Example 3:
  Input: x = 2.00000, n = -2
  Output: 0.25000
  Explanation: 2^-2 = (1/2)^2 = 1/4 = 0.25

Constraints:
  -100.0 < x < 100.0
  -2^31 <= n <= 2^31-1
  n is an integer.
  Either x is not zero or n > 0.
  -10^4 <= x^n <= 10^4
*/

class Solution {
public:
  static double myPow(double base, int e) {
    long exp = e;
    if (base == 0) return 0;
    if (exp == 0) return 1;
    if (std::abs(base) == 1)
      return (std::abs(exp) & 1) ? base : std::abs(base);
    if (exp < 0) {
      if (exp == std::numeric_limits<int>::min() and std::abs(base) < 1)
        return 0;
      exp = -exp;
      base = 1 / base;
    }
    if (exp == 1) return base;
    if (exp == 2) return base * base;

    uint exp_decay{ 1 };
    int rounds = std::floor(std::log2(exp));
    std::unordered_map<int, std::pair<double, int>> cache{ };
    double temp{ base };
    base = 1;
    for (int round = 0; round < rounds; ++round) {
      base *= temp;
      temp *= temp;
      exp_decay *= 2;
      cache[round] = { base, exp_decay - 1 };
    }
    exp -= cache.at(rounds - 1).second;
    std::pair<double, int> temp2;
    temp = cache.at(0).first;
    while (exp > 1) {
      rounds = std::floor(std::log2(exp));
      temp2 = cache.at(rounds - 1);
      temp *= temp2.first;
      exp -= temp2.second;
    }
    return base * temp;
  }
};

auto main(int argc, char **argv) -> int {
  if (argc <= 2) {
    std::cerr << "Usage: " << argv[0] << " base [exps...]"
      << "Example: 2 -5 10 -12 15"
      << R"(
Output:
  2 ^ -5 = 0.031250
  2.000000 ^ 10 = 1024.000000
  2.000000 ^ -12 = 0.000244
  2.000000 ^ 15 = 32768.000000
)";
    std::exit(1);
  }

  double base{ std::atof(argv[1]) };
  long number;

  for (int i = 2; i < argc; i++) {
    number = std::atol(argv[i]);
    std::cout << base << " ^ " << number
      << " = " << std::fixed << Solution::myPow(base, int(number)) << '\n';
  }
}
