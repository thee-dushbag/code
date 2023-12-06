#include <span>     // std::span
#include <cmath>    // std::log10, std::isnan, std::isinf, std::pow, std::max, std::floor
#include <limits>   // std::numeric_limits<int>
#include <string>   // std::string
#include <vector>   // std::vector<std::string>
#include <iomanip>  // std::quoted, std::setw, std::left
#include <iostream> // std::cout, std::cerr, std::size_t

/*
Implement the myAtoi(string s) function, which converts a string to a 32-bit signed
integer (similar to C/C++'s atoi function).

The algorithm for myAtoi(string s) is as follows:

Read in and ignore any leading whitespace.
Check if the next character (if not already at the end of the string) is '-' or
'+'. Read this character in if it is either. This determines if the final result
is negative or positive respectively. Assume the result is positive if neither is present.
Read in next the characters until the next non-digit character or the end of the
input is reached. The rest of the string is ignored.
Convert these digits into an integer (i.e. "123" -> 123, "0032" -> 32). If no digits
were read, then the integer is 0. Change the sign as necessary (from step 2).
If the integer is out of the 32-bit signed integer range [-2^31, 2^31 - 1], then clamp
the integer so that it remains in the range. Specifically, integers less than -2^31
should be clamped to -2^31, and integers greater than 2^31 - 1 should be clamped to 2^31 - 1.
Return the integer as the final result.
Note:

Only the space character ' ' is considered a whitespace character.
Do not ignore any characters other than the leading whitespace or the rest of the
string after the digits.

Example 1:

Input: s = "42"
Output: 42
Explanation: The underlined characters are what is read in, the caret is the
current reader position.
Step 1: "42" (no characters read because there is no leading whitespace)
         ^
Step 2: "42" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "42" ("42" is read in)
           ^
The parsed integer is 42.
Since 42 is in the range [-2^31, 2^31 - 1], the final result is 42.
*/

class Solution {
public:
  static int myAtoi(std::string const &s) {
    u_long found{ };
    u_long totalValue{ 1 };
    bool isNegative{ false }, firstChar{ true }, zeros{ true };
    for (char const &letter : s) {
      if (totalValue >= 1e11)
        return isNegative ? std::numeric_limits<int>::min() : std::numeric_limits<int>::max();
      if (letter == ' ') {
        if (not firstChar) break;
        continue;
      }
      if (firstChar) {
        if (letter == '-') {
          isNegative = true;
          firstChar = false;
          continue;
        }
        else if (letter == '+') {
          firstChar = false;
          continue;
        }
      }
      if ('0' <= letter and letter <= '9') {
        firstChar = false;
        if (letter == '0' and zeros)
          continue;
        zeros = false;
        found += ((letter - '0') * totalValue);
        totalValue *= 10;
        continue;
      }
      break;
    }
    u_long portion;
    int x_len{ digitCounter(totalValue - 1) }, index{ }, rindex{ x_len - 1 }, result{ };
    totalValue = 0;
    for (; index < x_len; ++index, --rindex) {
      portion = std::pow(10, rindex) * getIndexDigit(index, found);
      result += portion;
      totalValue += portion;
      if (totalValue > std::numeric_limits<int>::max())
        return isNegative ? std::numeric_limits<int>::min() : std::numeric_limits<int>::max();
    }
    return isNegative ? -result : result;
  }
  static int digitCounter(u_long x) {
    auto val = std::log10(x);
    if (std::isnan(val) or std::isinf(val)) return 0;
    return int(std::floor(val + 1));
  }
  static u_long getIndexDigit(int index, u_long number) {
    return u_long(std::floor(number * std::pow(10, -index))) % 10;
  }
};

auto main(int argc, char **argv) -> int {
  if (argc <= 1) {
    std::cerr << "Usage: " << argv[0] << " 123 -345 98765434567 -654345678765 'I am 20 years old.' '23rd century' '-13 degrees' '    -234' '  -123.456' '+-113   '"
      << R"(
Output:
  Input: "123"                | Output: 123
  Input: "-345"               | Output: -345
  Input: "98765434567"        | Output: 2147483647
  Input: "-654345678765"      | Output: -2147483648
  Input: "I am 20 years old." | Output: 0
  Input: "23rd century"       | Output: 23
  Input: "-13 degrees"        | Output: -13
  Input: "    -234"           | Output: -234
  Input: "  -123.456"         | Output: -123
  Input: "+-113   "           | Output: 0
)";
    std::exit(1);
  }
  std::vector<std::string> strings;
  std::size_t longest{ };

  for (std::string const &string : std::span{ argv + 1, argv + argc }) {
    longest = std::max(longest, string.length());
    strings.push_back(string);
  }
  longest += 2;
  for (std::string const &string : strings)
    std::cout << "Input: " << std::left << std::setw(longest) << std::quoted(string) << " | Output: " << Solution::myAtoi(string) << '\n';
}
