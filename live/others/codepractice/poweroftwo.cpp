#include <iomanip>
#include <iostream>

/*
Given an integer n, return true if it
is a power of two. Otherwise, return false.

An integer n is a power of two, if there
exists an integer x such that n == 2x.

Example 1:
  Input: n = 1
  Output: true
  Explanation: 20 = 1

Example 2:
  Input: n = 16
  Output: true
  Explanation: 24 = 16

Example 3:
  Input: n = 3
  Output: false
*/

struct Solution {
  static bool isPowerOfTwo(int n) {
    if (n <= 0) return false;
    return !(n & (n - 1));
  }
};

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 2 1 0 64 56 332 8766 4 8 9 10"
      << R"(
Output:
  number: 2           | isPowerOfTwo: true
  number: 1           | isPowerOfTwo: true
  number: 0           | isPowerOfTwo: false
  number: 64          | isPowerOfTwo: true
  number: 56          | isPowerOfTwo: false
  number: 332         | isPowerOfTwo: false
  number: 8766        | isPowerOfTwo: false
  number: 4           | isPowerOfTwo: true
  number: 8           | isPowerOfTwo: true
  number: 9           | isPowerOfTwo: false
  number: 10          | isPowerOfTwo: false
)";
    std::exit(1);
  }
  int number;
  std::cout << std::boolalpha;
  for (int i = 1; i < argc; i++) {
    number = std::atoi(argv[i]);
    std::cout << "number: " << std::setw(11) << std::left << number
      << " | isPowerOfTwo: " << Solution::isPowerOfTwo(number) << '\n';
  }
}