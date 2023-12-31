#include <vector>
#include <iostream>
#include <algorithm>
#include "helpers.hpp"
#include <unordered_map>

/*
Given an array of integers nums and an integer target,
find the indices of two integers in nums such that their
sum equals target.
Assume there is only one solution, ie only two integers
in nums can add upto target. Each integer in the list
can all be used once.
*/

struct Solution {
  static std::vector<int> twoSum(std::vector<int> const &nums, int target) {
    int i1{ 0 }, n2{ 0 };
    std::unordered_map<int, int> map;
    map.reserve(nums.size());

    for (auto ptr = nums.begin(); ptr != nums.end(); ptr++, i1++) {
      if(map.contains(*ptr) && (2 * *ptr) == target)
        return { map[*ptr], i1 };
      map[*ptr] = i1;
      n2 = target - *ptr;
      if (map.contains(n2) && map[n2] != i1)
        return { map[n2], i1 };
    }
    return { };
  }
};

auto main(int argc, char **argv) -> int {
  if (argc <= 3) {
    std::cerr << "Usage:\n"
      << '\t' << argv[0] << " [input...] target\n"
      << "where input and target are integers.\n"
      << "None integer values will be substituted for zeros.\n"
      << "Example: " << argv[0] << " 1 2 3 5 7\n"
      << R"(
Output:
  input    : [1, 2, 3, 5]
  target   : 7
  indicies : [1, 3]
  output   : [2, 5]
)";
    std::exit(1);
  }
  std::vector<int> nums;
  nums.reserve(argc);

  for (int i = 1; i < argc; i++)
    nums.push_back(std::atoi(argv[i]));

  int target = nums.back();
  nums.pop_back();
  auto indicies = Solution::twoSum(nums, target);
  std::vector<int> numbers;

  std::transform(
    std::cbegin(indicies),
    std::cend(indicies),
    std::back_inserter(numbers),
    [&nums](int const &index) { return nums[index]; }
  );
  std::cout << "input    : " << nums << '\n'
    << "target   : " << target << '\n'
    << "indicies : " << indicies << '\n'
    << "output   : " << numbers << '\n';
}