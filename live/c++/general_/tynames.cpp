#include <iostream>
#include <string>

auto main(int argc, char **argv) -> int {
  std::cout << typeid(char *).name() << '\n';
  std::cout << typeid(const char *).name() << '\n';
  std::cout << typeid(int).name() << '\n';
  std::cout << typeid(float).name() << '\n';
  std::cout << typeid(double).name() << '\n';
  std::cout << typeid(decltype(std::cout)).name() << '\n';
  std::cout << typeid(decltype(std::cerr)).name() << '\n';
  std::cout << typeid(decltype(std::clog)).name() << '\n';
  std::cout << typeid(std::string).name() << '\n';
  std::cout << typeid(std::string_view).name() << '\n';
  int y = 606;
}
