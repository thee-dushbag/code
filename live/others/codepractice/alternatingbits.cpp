#include <string>
#include <iostream>
#include <algorithm>

/*
Given a positive integer, check whether it has
alternating bits: namely, if two adjacent bits
will always have different values.

Example 1:
  Input: n = 5
  Output: true
  Explanation: The binary representation of 5 is: 101

Example 2:
  Input: n = 7
  Output: false
  Explanation: The binary representation of 7 is: 111
*/

std::string toBin(int number, std::size_t pad = 8) {
  uint num{ static_cast<uint>(number) };
  std::string bins{ "01" }, result;
  for (; num; num /= 2) result.push_back(bins[num % 2]);
  std::size_t len{ result.length() };
  for (; len < pad; len++) result.push_back('0');
  std::reverse(result.begin(), result.end());
  return result;
}

struct Solution {
  static bool hasAlternatingBits(int n) {
    uint setall{ n ^ (static_cast<uint>(n << 1) | !(n & 1)) };
    return !((setall + 1) & n);
  }
};

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 5 10 4 2 1 0 3 67 8"
      << R"(
Output:
  number: 5 | alternatingBits: true | bits: 101
  number: 10 | alternatingBits: true | bits: 1010
  number: 4 | alternatingBits: false | bits: 100
  number: 2 | alternatingBits: true | bits: 10
  number: 1 | alternatingBits: true | bits: 1
  number: 0 | alternatingBits: true | bits: 0
  number: 3 | alternatingBits: false | bits: 11
  number: 67 | alternatingBits: false | bits: 1000011
  number: 8 | alternatingBits: false | bits: 1000
)";
    std::exit(1);
  }

  std::cout << std::boolalpha;
  int number;
  for (int n = 1; n < argc; ++n) {
    number = std::atoi(argv[n]);
    std::cout << "number: " << number
      << " | alternatingBits: " << Solution::hasAlternatingBits(number)
      << " | bits: " << toBin(number, 1) << '\n';
  }
}