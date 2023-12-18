#include <vector>
#include <string>

struct Solution {
  std::vector<std::string> fizzBuzz(int const &n) {
    /*
    Given an integer n, return a string array answer (1-indexed) where:
    answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
    answer[i] == "Fizz" if i is divisible by 3.
    answer[i] == "Buzz" if i is divisible by 5.
    answer[i] == i (as a string) if none of the above conditions are true.
    */
    std::vector<std::string> fizzbuzz;
    fizzbuzz.reserve(n);
    for (int i = 1; i <= n; i++)
      fizzbuzz.emplace_back(
        (i % 3 == 0 and i % 5 == 0) ?
        "FizzBuzz" : (i % 3 == 0) ?
        "Fizz" : (i % 5 == 0) ?
        "Buzz" : std::to_string(i)
      );
    return fizzbuzz;
  }
};
