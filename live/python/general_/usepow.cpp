#include <iostream>
void hello();
int sum(int, int);
long double pow(long double, long);

auto main(int argc, char **argv) -> int {
  hello();
  sum(34, 55);
  std::cout << "2 ^ 10 = " << pow(2, 10) << '\n';
}
