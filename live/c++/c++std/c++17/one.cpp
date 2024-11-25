#include "string.hpp"
#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include <memory>
#include <string_view>
#include <tuple>
#include <utility>

using std::cout;

string get_name() { return "Simon Nganga Njoroge"; }
void print(string str) { cout << "str = '" << str.view() << "'\n"; }
void print(std::string_view str) { cout << "str = '" << str << "'\n"; }

void print(int const &a) { cout << "int& a = " << a << '\n'; }
void print(int const &&a) { cout << "int&& a = " << a << '\n'; }

template <class T>
void print_t(T &&a) {
  cout << "print<T>: ";
  print(std::forward<T>(a));
}

struct Print {
  static int operator()(int a, int b) {
    std::cout << a << " + " << b << " = " << a + b << '\n';
    return a + b;
  }
  static int operator()(int a) {
    std::cout << "-(" << a << ") = " << -a << '\n';
    return -a;
  }
};

struct arena_full : std::bad_alloc {
  const char *what() const noexcept override {
    return "arena_full: no more memory in arena";
  }
};

template <std::size_t N>
class StackArena {
  char memory[N];
  char *max, *top;
  std::size_t size;

public:
  StackArena(): memory(), max(memory + N), top(memory), size(N) { }
  template <typename T, typename... Args>
  T *allocate(Args &&...args) {
    if(top + sizeof(T) > max)
      throw arena_full();
    T *region = (T *)top;
    std::construct_at(region, std::forward<Args>(args)...);
    top += sizeof(T);
    return region;
  }

  template <typename T>
  void deallocate() { }
};

auto main(int argc, char **argv) -> int {
  StackArena<100> arena;
  std::unique_ptr<int, void (*)(int *)> age{arena.allocate<int>(100),
                                            [](int *) { }};
  std::cout << *age << '\n';

  return 0;
  typedef int BinaryOp(int, int);
  using UnaryOp = int(int);
  Print printop;
  BinaryOp *add = &Print::operator();
  add(90, 78);
  UnaryOp *neg = &Print::operator();
  neg(-67);
  return 0;
  auto val = std::make_tuple<string>("Simon", 'A', 56);
  string __name;
  char __grade;
  int __age;
  std::tie(__name, __grade, __age) = std::move(val);
  print_t(std::move(__name));
  return 0;
  string const &name = std::get<0>(val);
  const_cast<string &>(name).data()[0] = 'Z';
  /*name.data()[0] = 'S';*/
  /*print_t(std::move(name));*/
  print_t(std::get<0>(std::move(val)));
  std::cout << "Name is " << name.view() << '\n';
  return 0;
  auto names = std::make_pair<string, string>("Simon", "Nganga");
  /*std::pair<string, string> names{ "Simon", "Nganga" };*/
  print_t(std::move(names.first));
  print_t(std::move(names.second));
  return 0;
  print(9);
  int g = 10;
  print(g);
  print_t(9);
  print_t(g);
  return 0;
  string _name = get_name();
  cout << "Name: " << name.view() << '\n';
  print(name.view());
  print(std::move(name));
  cout << "Name: " << name.view() << '\n';
  cout << std::min({3, 4, 1, 2}) << '\n';
  cout << std::min({3, 1, 2011, 2014, -5}) << '\n';
  cout << std::min(-10, -5, [](int a, int b) {
    return std::abs(a) < std::abs(b);
  }) << '\n';
  cout << std::min({-11, -15, -13}, [](int a, int b) {
    return std::abs(a) < std::abs(b);
  }) << '\n';
  auto [min, max] = std::minmax({-7, -4, -3, -9, 10}, [](int a, int b) {
    return std::abs(a) < std::abs(b);
  });
  cout << "max: " << max << ", min: " << min << '\n';
}
