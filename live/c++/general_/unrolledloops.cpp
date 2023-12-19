#include <iostream>
#include <string>
#include <string_view>

#if defined(UNROLL) or defined(OPTALL)
# pragma GCC optimize("O3,unroll-loops")
#endif

void hello(std::string_view const &name) {
  for (int i = 1; i <= 5e6; i++)
    std::cout << i << ": Hello " << name << ", how was your day?\n";
}

auto main(int argc, char **argv) -> int {
#if defined(NOSYNC) or defined(OPTALL)
  std::ios::sync_with_stdio(false);
  std::cout.tie(nullptr);
  std::cin.tie(nullptr);
#endif
  hello("Simon Nganga");
}