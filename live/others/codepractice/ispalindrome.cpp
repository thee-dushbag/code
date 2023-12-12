#include <iostream>
#include <iostream>
#include <iomanip>

/*
Given an integer x, return true if x is a
palindrome, and false otherwise.

Example 1:
  Input: x = 121
  Output: true
  Explanation: 121 reads as 121 from left to right and from
  right to left.

Example 2:
  Input: x = -121
  Output: false
  Explanation: From left to right, it reads -121. From
  right to left, it becomes 121-. Therefore it is not a palindrome.

Example 3:
  Input: x = 10
  Output: false
  Explanation: Reads 01 from right to left. Therefore it is
  not a palindrome.
*/

struct Solution {
  static bool isPalindrome(int const &number) {
    if (number < 10) return number >= 0;
    uint reversed{ 0 };
    for (int temp = number; temp; temp /= 10)
      reversed = (reversed * 10) + (temp % 10);
    return reversed == static_cast<uint>(number);
  }
};

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " [numbers...]\n"
      << "Example: " << argv[0] << " 121 123 1234321 -989 67576 656787"
      << R"(
Output:
  isPalindrome: true  | number: 121
  isPalindrome: false | number: 123
  isPalindrome: true  | number: 1234321
  isPalindrome: false | number: -989
  isPalindrome: true  | number: 67576
  isPalindrome: false | number: 656787
)";
    std::exit(1);
  }
  int number;
  std::cout << std::boolalpha;
  for (int i = 1; i < argc; i++) {
    number = std::atoi(argv[i]);
    std::cout << "isPalindrome: " << std::setw(5)
      << std::left << Solution::isPalindrome(number)
      << " | number: " << number << '\n';
  }
}