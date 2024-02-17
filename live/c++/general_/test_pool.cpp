#include <iostream>
#include <snn_pool.hpp>
#include <string>

using std::string_literals::operator""s;

auto main(int argc, char **argv) -> int {
  snn::Pool pool{ 1 };
  auto add = [](int x, int y) { std::cout << "T1\n"; return x + y; };
  auto mul = [](int x, int y) { return x * y; };
  snn::Task t1{ add, 3, 4 };
  auto task = [&add] -> int { std::cout << "5 + 6 = " << add(5, 6) << '\n'; return add(5, 6); };
  pool.put_task(task);
  auto hello = [](std::string const &name) { std::cout << "Hello " << name << "!!!\n"; };
  snn::Task t2{ hello, "Simon Nganga"s };
  pool.put_task(t1);
  pool.put_task(t2);
  std::cout << "Wait for t1.\n";
  std::cout << "Result: " << t1.get() << '\n';
}
