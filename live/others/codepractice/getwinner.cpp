#include <iostream>
#include <vector>
#include "helpers.hpp"
#include <algorithm>
#include <chrono>
#include <thread>

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
  static int getWinner(std::vector<int>& arr, int k) {
    int score = 0;
    while (score != k)
      score = _switch(arr, score);
    return arr[0];
  }

private:
  static int _switch(std::vector<int>& arr, int score) {
    if (arr[0] > arr[1]) {
      std::swap(arr[0], arr[1]);
      score++;
    }
    else
      score = 1;
    int temp = arr.front();
    arr.erase(arr.begin());
    arr.push_back(temp);
    return score;
  }
};

auto main(int argc, char** argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage:\n"
      << '\t' << argv[0] << " [input...] score\n"
      << "where input and target are integers.\n"
      << "None integer values will be substituted for zeros.\n"
      << "Example: " << argv[0] << " 2 1 3 5 4 6 7 2\n"
      << R"(
Output:
  input  : [2, 1, 3, 5, 4, 6, 7]
  score  : 2
  output : [5, 6, 7, 1, 2, 3, 4]
  winner : 5
)";
    std::exit(1);
  }

  std::vector<int> input;
  input.reserve(argc);
  for (int i = 1; i < argc; i++)
    input.push_back(std::atoi(argv[i]));

  int score = input.back();
  input.pop_back();

  std::vector<int> output = input;

  int winner = Solution::getWinner(output, score);

  std::cout << "input  : " << input << '\n'
    << "score  : " << score << '\n'
    << "output : " << output << '\n'
    << "winner : " << winner << '\n';
}