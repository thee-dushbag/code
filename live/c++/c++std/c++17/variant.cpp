#include "variant.hpp"
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <string_view>

using std::cout;

void *operator new(std::size_t size) {
  cout << "Alloc:  " << size << '\n';
  return std::malloc(size);
}

std::optional<std::string_view> get_name() {
  if(std::rand() > RAND_MAX * 0.5)
    return "Simon Nganga";
  return std::nullopt;
}

struct Object {
  Object() { std::cout << "Object(init)\n"; }
  ~Object() { std::cout << "Object(term)\n"; }
};

std::ostream &operator<<(std::ostream &out, Object const &o) {
  return out << "Object(print)";
}

#define TEST(expr)                                                             \
  do                                                                           \
    try {                                                                      \
      (expr);                                                                  \
      std::cout << "Success: " #expr "\n";                                     \
    } catch(...) {                                                             \
      std::cout << "Failed: " #expr "\n";                                      \
    }                                                                          \
  while(false)

int main() {
  variant<float, char, double> value;
  TEST(value.get<char>());
  TEST(value.get<float>());
  TEST(value.get<double>());

  struct {
    void operator()(int &a) { std::cout << "Visit(Int): " << a << '\n'; }
    void operator()(char &a) { std::cout << "Visit(Char): " << a << '\n'; }
    void operator()(double &a) { std::cout << "Visit(Double): " << a << '\n'; }
    void operator()(Object &a) { std::cout << "Visit(Other): " << a << '\n'; }
  } funcs;
  variant<int, double, char, Object> v('5');
  std::cout << "Char: " << v.get<char>() << '\n';
  visit(v, funcs);
  v = 56.78;
  std::cout << "Double: " << v.get<double>() << '\n';
  visit(v, funcs);
  v = 5052;
  /*std::cout << "Int: " << v.get<int>() << '\n';*/
  visit(v, funcs);
  v = Object();
  /*std::cout << "Other: " << v.get<Object>() << '\n';*/
  visit(v, funcs);
  v.destroy();
  TEST(visit(v, funcs));
  return 0;
  std::srand(std::time(nullptr));
  auto name = get_name();
  std::cout << name.value_or("[No Name]") << " is a beautiful name.\n";
  for(int i : {1, 2, 3, 4, 5})
    if(auto name = get_name(); name.has_value())
      std::cout << "Your name is " << *name << '\n';
    else
      std::cout << "Name not found!\n";
  return 0;
  std::vector<int> big_vec(500'000'000, 2011), empty;
  cout << "Expect: " << big_vec.size() * 4 << '\n';
  auto begin = std::chrono::high_resolution_clock::now();
  empty = std::move(big_vec); // Copy
  auto lapse = std::chrono::high_resolution_clock::now() - begin;

  auto lapse_seconds = std::chrono::duration<double>(lapse).count();
  cout << lapse_seconds << '\n';
}
