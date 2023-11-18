#include <iostream>
#include <optional>

auto main(int argc, char **argv) -> int {
  std::optional<int> i { 20 };
  i = i.transform([](int i) { return i * i; });
  std::cout << "i = " << i.value_or(-1) << '\n';
}