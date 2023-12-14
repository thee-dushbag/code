#include <iostream>
#include <string>
#include <iomanip>

/*
Too simple to termify or document (-_-)
*/

struct Solution {
  static int lengthOfLastWord(std::string const &s) {
    int size{ };
    bool spaces{ s.back() == ' ' };
    for (auto ch = s.crbegin(); ch != s.crend(); ++ch)
      if (*ch == ' ') { if (not spaces) break; }
      else { spaces = false; ++size; }
    return size;
  }
};

auto main(int argc, char **argv) -> int {
  std::cout << std::boolalpha;
  for (std::string string : {
    "My name is Simon",
      "I want to go to spaces   ",
      "the    mooon   is   big   ",
      "     singe night      "
  })
    std::cout << std::quoted(string) << " = "
      << Solution::lengthOfLastWord(string) << '\n';
}