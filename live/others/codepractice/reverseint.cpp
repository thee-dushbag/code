#include <iostream>
#include <cmath>
#include <vector>
#include <limits>
#include <iomanip>

class Solution {
public:
  static int digitCounter(int x) {
    if (x == 0) return 0;
    auto val = std::log10(x);
    if (std::nan(val) or std::isinf(val)) return 0;
    return int(std::floor(val + 1));
  }
  static int getIndexDigit(int index, int number) {
    return int(std::floor(number * std::pow(10, -index))) % 10;
  }
  static int reverse(int x) {
    bool isNegative = (x < 0);
    x = std::abs(x);
    long portion;
    int result{ }, digit, x_len{ digitCounter(x) };
    // std::cout << "Max: " << std::numeric_limits<int>::max() << " | x: " << x << '\n';
    for (int index = 0; index < x_len; ++index) {
      digit = getIndexDigit(index, x);
      portion = std::pow(10, x_len - index - 1) * digit;
      if (portion > std::numeric_limits<int>::max()) return 0;
      result += portion;
      if (result < 0) return 0;
      // std::cout << "Current: " << std::setw(x_len) << result
      //     << " | Digit: " << digit <<  " | portion: "
      //     << std::setw(x_len) << portion << '\n';
    }
    if (result < 0) return 0;
    if (isNegative) result = -result;
    if (isNegative && result >= 0) return 0;
    return result;
  }
};


auto main(int argc, char **argv) -> int {
  if (argc == 1) {
    std::exit(1);
  }
  std::vector<int> numbers;
  for (int i = 1; i < argc; i++)
    numbers.push_back(std::atoi(argv[i]));
    int i = 0;
  for (int number : numbers) {
    i++;
    std::cout << "String: " << argv[i]
      << " | Input: " << number
      << " | Output: " << Solution::reverse(number) << '\n';
  }
}
