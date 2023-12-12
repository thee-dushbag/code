#include <iostream>
#include <string>
#include <iomanip>
#include <algorithm>

/*
Given an integer num, return a string representing
its hexadecimal representation. For negative integers,
two’s complement method is used.

All the letters in the answer string should be lowercase
characters, and there should not be any leading zeros
in the answer except for the zero itself.

Note: You are not allowed to use any built-in library
method to directly solve this problem.

Example 1:
  Input: num = 26
  Output: "1a"
*/

struct Solution {
  static std::string toHex(int n) {
    if (n == 0) return "0";
    uint num{ static_cast<uint>(n) };
    std::string hexes{ "0123456789abcdef" }, result;
    for (; num; num /= 16) result.push_back(hexes[num % 16]);
    std::reverse(result.begin(), result.end());
    return result;
  }
};

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 76 65 986545 542 514 0 -75 -644 2 7655 -987654 8626"
      << R"(
Output:
  number: 76          | hex: 4c
  number: 65          | hex: 41
  number: 986545      | hex: f0db1
  number: 542         | hex: 21e
  number: 514         | hex: 202
  number: 0           | hex: 0
  number: -75         | hex: ffffffb5
  number: -644        | hex: fffffd7c
  number: 2           | hex: 2
  number: 7655        | hex: 1de7
  number: -987654     | hex: fff0edfa
  number: 8626        | hex: 21b2
)";
    std::exit(1);
  }
  int number;
  for (int i = 1; i < argc; i++) {
    number = std::atoi(argv[i]);
    std::cout << "number: " << std::setw(11) << std::left << number
      << " | hex: " << Solution::toHex(number) << '\n';
  }
}