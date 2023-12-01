#include <iostream>
#include <cmath>
#include <vector>
#include <limits>
#include <iomanip>
#include <string_view>

/*
Given a signed 32-bit integer x, return x with
its digits reversed. If reversing x causes the
value to go outside the signed 32-bit integer
range [-231, 231 - 1], then return 0.

Assume the environment does not allow you
to store 64-bit integers (signed or unsigned).

Example 1:
  Input: x = 123
  Output: 321

Example 2:
  Input: x = -123
  Output: -321

Example 3:
  Input: x = 120
  Output: 21

Constraints:
  -2^31 <= x <= 2^31 - 1
*/

class Solution {
public:
  static int digitCounter(int x) {
    if (x <= 0) return 0;
    auto val = std::log10(x);
    if (std::isnan(val) or std::isinf(val)) return 0;
    return int(std::floor(val + 1));
  }
  static int getIndexDigit(int index, int number) {
    return int(std::floor(number * std::pow(10, -index))) % 10;
  }
  static int reverse(int x) {
    bool isNegative = (x < 0);
    x = std::abs(x);
    long portion;
    int result{ }, x_len{ digitCounter(x) }, index { }, rindex { x_len - 1 };
    for (; index < x_len; ++index, --rindex) {
      portion = std::pow(10, rindex) * getIndexDigit(index, x);
      if (portion > std::numeric_limits<int>::max()) return 0;
      result += portion;
      if (result < 0) return 0;
    }
    return isNegative? -result: result;
  }
};


auto main(int argc, char **argv) -> int {
  if (argc == 1) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 4321 -98767 1023456789"
      << R"(
Output:
  String: "1234"       | Input: 1234         | Output: 4321        
  String: "-98767"     | Input: -98767       | Output: -76789      
  String: "1023456789" | Input: 1023456789   | Output: 0           
)";
    std::exit(1);
  }
  std::vector<int> numbers;
  std::size_t maxlen = 0;
  for (int i = 1; i < argc; i++) {
    numbers.push_back(std::atoi(argv[i]));
    maxlen = std::max(std::string_view(argv[i]).size(), maxlen);
  }
  maxlen += 2;
  int i{ 1 };
  std::vector<int>::const_iterator iter{ numbers.cbegin() };
  for (; iter != numbers.cend(); ++iter, ++i)
    std::cout << std::left
    << "String: " << std::setw(maxlen) << std::quoted(argv[i])
    << " | Input: " << std::setw(maxlen) << *iter
    << " | Output: " << std::setw(maxlen) << Solution::reverse(*iter) << '\n';
}
