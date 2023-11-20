#include <bitset>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "helpers.hpp"

/*
Longest Substring Without Repeating Characters
-----------------------------------------------
Given a string s, find the length of the longest 
substring
 without repeating characters.

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
 

Constraints:

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.
*/

class Solution {
public:
  std::vector<std::string> substrings { };

  int lengthOfLongestSubstring(std::string s) {
    int longest_size{ 0 };
    std::size_t temp_size{ 0 };
    std::bitset<256> seen;
    std::string substr{ };
    std::size_t remaining = s.length();
    seen.reset();
    for (std::string::iterator ch = s.begin(); ch != s.end(); ++ch) {
      for (std::string::iterator ch2 = ch; ch2 != s.end(); ++ch2) {
        if (seen.test(*ch2))
          break;
        else {
          temp_size++;
          seen.flip(*ch2);
        }
        substr.push_back(*ch2);
      }
      substrings.push_back(substr);
      substr = "";
      remaining--;
      if (temp_size > longest_size)
        longest_size = temp_size;
      // if (longest_size > remaining) break; // Uncomment for optimization
      seen.reset();
      temp_size = 0;
    }
    return longest_size;
  }
};

auto main(int argc, char **argv) -> int {
  if (argc == 1) {
    std::cerr << "Usage: " << argv[0] << " [strings...]\n"
    << "Find the longest substring with no repeating chars.\n"
    << "Example: " << argv[0] << " abcabcbb"
    << R"(
  input:      'abcabcbb'
  substrings: [abc, bca, cab, abc, bc, cb, b, b]
  longest:    [abc, bca, cab, abc]
  size:       3
)";
    std::exit(1);
  }
  Solution soln;
  int size;
  std::vector<std::string> winners;
  for (int i = 1; i < argc; i++) {
    size = soln.lengthOfLongestSubstring(argv[i]);
    std::for_each(
      soln.substrings.begin(), soln.substrings.end(),
      [&winners, &size](std::string const&str)
      { if(str.length() >= size) winners.push_back(str); }
    );
    std::cout << "input:      '" << argv[i] << "'\n";
    std::cout << "substrings: " << soln.substrings << '\n';
    std::cout << "longest:    " << winners << '\n';
    std::cout << "size:       " << size << "\n\n";
    soln.substrings.clear();
    winners.clear();
  }
}
