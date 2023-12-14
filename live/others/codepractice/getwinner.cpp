#include <iostream>
#include <vector>
#include <deque>
#include "helpers.hpp"
#include <algorithm>

/*
Given an integer array arr of distinct integers and an integer k.
A game will be played between the first two elements of the array
(i.e. arr[0] and arr[1]). In each round of the game, we compare
arr[0] with arr[1], the larger integer wins and remains at position 0,
and the smaller integer moves to the end of the array. The game
ends when an integer wins k consecutive rounds.
Return the integer which will win the game.

All integers in array are unique.
*/

struct Solution {
  static int getWinner(std::vector<int> &arr, int k) {
    if (k  > (arr.size() / 2))
      return std::ranges::max(arr);
    std::deque<int> darr{ arr.begin(), arr.end() };
    int score{ };
    while (score < k) {
      if (darr[0] > darr[1]) {
        std::swap(darr[0], darr[1]);
        score++;
      }
      else score = 1;
      darr.push_back(darr.front());
      darr.pop_front();
    }
    return darr[0];
  }
};

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage:\n"
      << '\t' << argv[0] << " score [input...]\n"
      << "where input and target are integers.\n"
      << "None integer values will be substituted for zeros.\n"
      << "Example: " << argv[0] << " 2 2 1 3 5 4 6 7\n"
      << R"(
Output:
  input  : [2, 1, 3, 5, 4, 6, 7]
  score  : 2
  output : [5, 6, 7, 1, 2, 3, 4]
  winner : 5
)";
    std::exit(1);
  }

  std::vector<int> input(argc - 2);
  int score = std::atoi(argv[1]);

  for (int i = 2; i < argc; i++)
    input[i - 2] = std::atoi(argv[i]);

  std::vector<int> output = input;
  int winner = Solution::getWinner(output, score);

  std::cout << "input  : " << input << '\n'
    << "score  : " << score << '\n'
    << "output : " << output << '\n'
    << "winner : " << winner << '\n';
}