#include <vector>
#include <iostream>
#include <algorithm>

struct Solution {
  std::vector<int> twoSum(std::vector<int>& nums, int target) {
    std::vector<int> result;
    for (int a = 0; a < nums.size(); a++) {
      for (int b = 0; b < nums.size(); b++) {
        if ((nums[a] + nums[b]) == target && nums[a] != nums[b]) {
          result.push_back(a);
          result.push_back(b);
          break;
        }
      }
      if (result.size() == 2)
        break;
    }
    return result;
  }
};

template<class T>
void print(std::vector<T> const& vec) {
  std::cout << '[';
  for (const auto& t : vec)
    std::cout << t << ',';
  std::cout << "]\n";
}

auto main(int argc, char** argv) -> int {
  std::vector<int> nums{ 3,2,4 };
  int target = 6;
  std::cout << "nums: ";
  print(nums);
  std::cout << "target: " << target << '\n';
  Solution sol;
  auto indicies = sol.twoSum(nums, target);
  std::cout << "indicies: ";
  print(indicies);
  std::vector<int> numbers;
  std::transform(
    std::cbegin(indicies),
    std::cend(indicies),
    std::back_inserter(numbers),
    [&nums](int const& index) { return nums[index]; }
  );
  std::cout << "numbers: ";
  print(numbers);
}