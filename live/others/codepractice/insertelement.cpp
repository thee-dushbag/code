#include <set>
#include <cmath>
#include <vector>
#include <iostream>
#include <algorithm>
#include "helpers.hpp"

/*
Given a sorted array of distinct integers and a target value,
return the index if the target is found. If not, return the
index where it would be if it were inserted in order.s
You must write an algorithm with O(log n) runtime complexity.

Example 1:
  Input: nums = [1,3,5,6], target = 5
  Output: 2
*/

struct Solution {
  static inline int searchInsert(std::vector<int> &nums, int target) {
    if (not nums.size() or nums.front() > target) return 0;
    if (target > nums.back()) return static_cast<int>(nums.size());
    int index{ static_cast<int>(nums.size() - 1) };
    auto current{ nums.crbegin() };
    for (;current != nums.crend(); ++current, --index)
      if (*current <= target) break;
    return (nums[index] == target) ? index : index + 1;
  }
};

std::vector<int> insertAt(std::vector<int> array, int target, int index) {
  std::vector<int> nums{ array };
  if (index == 0) nums.insert(nums.begin(), target);
  else if (static_cast<std::size_t>(index) == nums.size()) nums.push_back(target);
  else for (auto iter = nums.begin(); iter != nums.end(); iter++, index--)
    if (index == 0) { if (*iter != target) nums.insert(iter, target); break; }
  return nums;
}

auto main(int argc, char **argv) -> int {
  if (argc <= 3) {
    std::cerr << "Usage: " << argv[0] << " [target] [numbers...]\n"
      << "Example: " << argv[0] << " 2 1 3 5 6"
      << R"(
Output:
  target: 2
  input : [1, 3, 5, 6]
  index : 1
  output: [1, 2, 3, 5, 6]
)";
    std::exit(1);
  }
  int target{ std::atoi(argv[1]) };
  std::vector<int> numbers;
  bool inArray{ false };
  {
    for (int i = 2; i < argc; i++)
      numbers.push_back(std::atoi(argv[i]));

    if (not std::is_sorted(numbers.cbegin(), numbers.cend())) {
      std::cout << "sorting: " << numbers << '\n';
      std::sort(numbers.begin(), numbers.end());
    }
    std::set<int> unique{ numbers.begin(), numbers.end() };
    inArray = unique.contains(target);
    if (unique.size() < numbers.size()) {
      numbers.clear();
      numbers = { unique.begin(), unique.end() };
      std::cout << "crashing: " << numbers;
    }
  }
  int index = Solution::searchInsert(numbers, target);
  std::cout << "target: " << target << '\n'
    << "input : " << numbers << '\n'
    << "index : " << index << '\n'
    << "output: " << (inArray ? numbers : insertAt(numbers, target, index)) << '\n';
}