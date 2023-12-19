#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include "helpers.hpp"

struct Solution {
  static std::vector<std::vector<int>> imageSmoother(std::vector<std::vector<int>> const &img) {
    /*
    An image smoother is a filter of the size 3 x 3
    that can be applied to each cell of an image by
    rounding down the average of the cell and the
    eight surrounding cells (i.e., the average of the
    nine cells in the blue smoother). If one or more
    of the surrounding cells of a cell is not present,
    we do not consider it in the average (i.e., the
    average of the four cells in the red smoother).

    Given an m x n integer matrix img representing
    the grayscale of an image, return the image after
    applying the smoother on each cell of it.

    m == img.length
    n == img[i].length
    1 <= m, n <= 200
    0 <= img[i][j] <= 255
    */
    const std::size_t rows{ img.size() }, columns{ img[0].size() };
    int total{ 0 }, count{ 0 }, row, column, r, c;
    std::vector<std::vector<int>> smoothed(rows, std::vector<int>(columns));
    for (row = 0; row < rows; ++row)
      for (column = 0; column < columns; ++column, total = count = 0) {
        for (r = row - (row > 0); r <= row + (row + 1 < rows); ++r)
          for (c = column - (column > 0); c <= column + (column + 1 < columns); ++c, ++count)
            total += img[r][c];
        smoothed[row][column] = std::floor(total / count);
      }
    return smoothed;
  }

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


using image_type = std::vector<std::vector<int>>;

auto main(int argc, char **argv) -> int {
  std::vector<image_type> images{
    {{1, 2, 3},{4, 5, 6},{7, 8, 9}},
    {{11, 12, 13},{14, 15, 16},{17, 18, 19}},
    {{12, 42, 34, 46},{35, 63, 23, 43},{98, 23, 92, 11}},
    {{255, 254, 253},{45, 89, 34},{56, 32, 67},{46, 79, 53},{45, 32, 67},{34, 43, 56}}
  };
  for (image_type const &image : images)
    std::cout << "image: " << image << " | smoothed: "
    << Solution::imageSmoother(image) << '\n';
}