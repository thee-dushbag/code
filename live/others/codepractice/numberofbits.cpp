#include <cmath>
#include <iomanip>
#include <iostream>

/*
Write a function that takes the binary representation
of an unsigned integer and returns the number of '1' bits
it has (also known as the Hamming weight).
*/

struct Solution {
  static int hammingWeight(uint n) {
    if (n == 0) return 0;
    int l = std::floor(std::log2(n) + 1), r{ };
    for (int i = 0; i < l; i++) r += bool(n & (1 << i));
    return r;
  }
};

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 3 76 65 756 542 514 0 2 7655 8626"
      << R"(
Output:
  number: 3           | count: 2
  number: 76          | count: 3
  number: 65          | count: 2
  number: 756         | count: 6
  number: 542         | count: 5
  number: 514         | count: 2
  number: 0           | count: 0
  number: 2           | count: 1
  number: 7655        | count: 10
  number: 8626        | count: 6
)";
    std::exit(1);
  }
  int number;
  for (int i = 1; i < argc; i++) {
    number = std::atoi(argv[i]);
    std::cout << "number: " << std::setw(11) << std::left << number
      << " | count: " << Solution::hammingWeight(number) << '\n';
  }
}
