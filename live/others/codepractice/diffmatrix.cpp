#include <iostream>
#include <vector>
#include <algorithm>
#include "helpers.hpp"
#include <cmath>

/*
You are given a 0-indexed m x n binary matrix grid.

A 0-indexed m x n difference matrix diff is created
with the following procedure:

Let the number of ones in the ith row be onesRowi.
Let the number of ones in the jth column be onesColj.
Let the number of zeros in the ith row be zerosRowi.
Let the number of zeros in the jth column be zerosColj.

diff[i][j] = onesRowi + onesColj - zerosRowi - zerosColj

Return the difference matrix diff.
*/

struct Solution {
  static std::vector<std::vector<int>> &onesMinusZeros(std::vector<std::vector<int>> &grid) {
    std::size_t rows{ grid.size() }, columns{ grid[0].size() }, row, column, temp;
    std::vector<int> rows_diff(rows), columns_diff(columns);
    for (row = 0; row < rows; row++)
      for (column = 0; column < columns; column++) {
        temp = grid[row][column] ? 1 : -1;
        rows_diff[row] += temp;
        columns_diff[column] += temp;
      }
    for (row = 0; row < rows; row++)
      for (column = 0; column < columns; column++)
        grid[row][column] = rows_diff[row] + columns_diff[column];
    return grid;
  }
};



std::ostream &operator<<(std::ostream &out, std::vector<std::vector<int>> const &matrix) {
  out << '[';
  for (auto &row : matrix) {
    out << row;
    if (&row != &matrix.back()) out << ", ";
  }
  return out << ']';
}

auto main(int argc, char **argv) -> int {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " [[numbers...]...]\n"
      << "Note: numbers will be converted to 1 or 0 and into a matrix of the lower sqrt size\n"
      << "Example: " << argv[0] << " 0 1 3 4 0 1 0 0 1"
      << R"(
Output:
  numbers: [0, 1, 1, 1, 0, 1, 0, 0, 1]
  size: 3x3
  matrix: [[0, 1, 1], [1, 0, 1], [0, 0, 1]]
  diffs:  [[0, 0, 4], [0, 0, 4], [-2, -2, 2]]
)";
    std::exit(1);
  }
  std::vector<bool> numbers;
  for (int i = 1; i < argc; i++)
    numbers.push_back(std::atoi(argv[i]));
  double matrix_size{ std::floor(std::sqrt(argc - 1)) };
  std::cout << "numbers: " << numbers << '\n'
    << "size: " << matrix_size << "x" << matrix_size << '\n';
  std::vector<std::vector<int>> matrix(matrix_size);
  for (int row = 0; row < matrix_size; row++)
    for (int column = 0; column < matrix_size; column++)
      matrix[row].push_back(numbers[(row * matrix_size) + column]);
  std::cout << "matrix: " << matrix << '\n'
    << "diffs:  " << Solution::onesMinusZeros(matrix) << '\n';
}