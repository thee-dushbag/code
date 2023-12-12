#include <vector>
#include <iostream>
#include "helpers.hpp"

/*
You are given a large integer represented as an integer
array digits, where each digits[i] is the ith digit of
the integer. The digits are ordered from most significant
to least significant in left-to-right order. The large
integer does not contain any leading 0's.

Increment the large integer by one and return the
resulting array of digits.

Example 1:
  Input: digits = [1,2,3]
  Output: [1,2,4]
  Explanation: The array represents the integer 123.
  Incrementing by one gives 123 + 1 = 124.
  Thus, the result should be [1,2,4].

Example 2:
  Input: digits = [4,3,2,1]
  Output: [4,3,2,2]
  Explanation: The array represents the integer 4321.
  Incrementing by one gives 4321 + 1 = 4322.
  Thus, the result should be [4,3,2,2].
*/

struct Solution {
  static std::vector<int> plusOne(std::vector<int> &digits) {
    std::vector<int>::reverse_iterator digit{ digits.rbegin() };
    digits.back() += 1;
    bool carry{ };

    for (auto digit = digits.rbegin(); digit != digits.rend(); ++digit) {
      *digit += carry; carry = *digit >= 10; *digit %= 10;
      if (not carry) break;
    }

    if (carry) digits.insert(digits.begin(), 1);
    return digits;
  }
};

std::vector<int> vectorize(std::string number) {
  std::vector<int> digits;
  for (char ch : number)
    if (std::isdigit(ch))
      digits.push_back(ch - '0');
    else digits.push_back(0);
  return digits;
}

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 1234 9999 43456 76251 87567 4323 00999"
      << R"(
Output:
  number: [1, 2, 3, 4] | output: [1, 2, 3, 5]
  number: [9, 9, 9, 9] | output: [1, 0, 0, 0, 0]
  number: [4, 3, 4, 5, 6] | output: [4, 3, 4, 5, 7]
  number: [7, 6, 2, 5, 1] | output: [7, 6, 2, 5, 2]
  number: [8, 7, 5, 6, 7] | output: [8, 7, 5, 6, 8]
  number: [4, 3, 2, 3] | output: [4, 3, 2, 4]
  number: [0, 0, 9, 9, 9] | output: [0, 1, 0, 0, 0]
)";
    std::exit(1);
  }
  std::vector<int> number;
  for (int i = 1; i < argc; ++i) {
    number = vectorize(argv[i]);
    std::cout << "number: " << number << " | output: " << Solution::plusOne(number) << '\n';
  }
}