/*
Given a non-negative integer x, return the square root of x
rounded down to the nearest integer. The returned integer
should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

Example 1:

Input: x = 4
Output: 2
Explanation: The square root of 4 is 2, so we return 2.

Example 2:

Input: x = 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we
round it down to the nearest integer, 2 is returned.

Constraints:

0 <= x <= 2^31 - 1
*/

#include <iostream>
#include <cmath>
#include <span>
#include <vector>


struct Solution {
  static int mySqrt(int x) {
    if (x < 0) return 0;
    const uint u = static_cast<uint>(x) + 1;
    double last_y{ static_cast<double>(x) }, cur_y{ last_y / 2 }, cur_sqr, extent;
    auto found = [&x, &u](auto s) -> bool { return u > s and s >= x; };
    while (not found((cur_sqr = cur_y * cur_y))) {
      extent = std::abs(last_y - cur_y) / 2;
      last_y = cur_y;
      if (cur_sqr > x) cur_y -= extent;
      else if (cur_sqr < x) cur_y += extent;
      else break;
    }
    return std::floor(cur_y);
  }
};

auto main(int argc, char **argv) -> int {
  if (argc <= 1) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 113 99 100 1 12345 10000 4 0"
      << R"(
Output:
  floor(sqrt(113)) = 10
  floor(sqrt(99)) = 9
  floor(sqrt(100)) = 10
  floor(sqrt(1)) = 1
  floor(sqrt(12345)) = 111
  floor(sqrt(10000)) = 100
  floor(sqrt(4)) = 2
  floor(sqrt(0)) = 0
)";
    std::exit(1);
  }
  int result;
  std::vector<float> numbers;
  for (const char *arg : std::span{ argv + 1, argv + argc })
    numbers.push_back(std::atof(arg));
  for (auto &number : numbers)
    std::cout << "floor(sqrt(" << number << ")) = " << Solution::mySqrt(number) << '\n';
}
