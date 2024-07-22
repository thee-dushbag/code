#include <iostream>
#include <type_traits>
#include <utility>
#include <functional>
#include <string_view>

template<typename T>
std::function<T()> param(std::string_view const &name, T &&value) {
  return [=] -> T {
    std::cout << "Read Param: " << name << ": " << value << '\n';
    return value;
  };
}

enum class Bool: char { False, True, Indeterminate };

template<typename T>
void hello(T const &) { std::cout << "Hello World\n"; }

[[deprecated("hello<char> is unsupported, use any other type.")]]
void hello(char const &) { std::cout << "I said, STOP IT!!!\n"; }

[[nodiscard]]
int add(int x, int y) { return x + y; }

void vote(int age) {
  [[unlikely]] if ( age > 100 ) std::cout << "Age too big.\n";
  else [[likely]] if ( age >= 18 ) std::cout << "You can vote.\n";
  else [[unlikely]] if ( age >= 0 ) std::cout << "You are underage, please go home.\n";
  else std::cout << "Age too small.\n";
}

namespace std {
  string to_string(Bool const &b) {
#define case_bool(value) case value: return #value
    switch ( b ) {
      using enum Bool;
      case_bool(False);
      case_bool(True);
      case_bool(Indeterminate);
      default: unreachable();
    }
#undef case_bool
  }
  ostream &operator<<(ostream &out, Bool const &b) {
    return out << to_string(b);
  }
}

template<typename T>
decltype(auto) add(T &&a, T &&b, T &&c) { return a + b + c; }

auto main(int argc, char **argv) -> int {
  // for (uint i = 0; i < 20'000'000; ++i)
  //   std::cout << i << '\n';
  hello(2);
  hello(9.9);
  hello('h');
  int i = add(9, 8);
  vote(9);
  vote(100);
  vote(23);
  std::cout << i << '\n';
  std::cout
    << Bool::True << '\n'
    << Bool::False << '\n'
    << Bool::Indeterminate << '\n';
  auto
    a = param("a", 1),
    b = param("b", 2),
    c = param("c", 3);
  std::cout << add(a(), b(), c()) << '\n';
}
