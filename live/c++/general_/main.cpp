#include <iostream>
#include "events.hpp"
#include <mutex>

std::mutex gmut;

template <typename... T>
void print(const T &...t) {
  gmut.lock();
  (std::cout << ... << t) << '\n';
  gmut.unlock();
}

using namespace std::string_literals;

int add(int x, int y) {
  print(x, " + ", y, " = ", x + y);
  return x + y;
}
int mul(int x, int y) {
  print(x, " * ", y, " = ", x * y);
  return x * y;
}
int sub(int x, int y) {
  print(x, " - ", y, " = ", x - y);
  return x - y;
}

struct xy_param {
  int x, y;
  xy_param(int x, int y) : x{ x }, y{ y } { }
  void set(int x, int y) {
    this->x = x;
    this->y = y;
  }
};

std::string say_hi(const std::string &name) {
  print("Hello ", name, ", how was your day?");
  return name;
}

int xy_hooker(int (*function)(int, int), xy_param &param) {
  return function(param.x, param.y);
}

using xy_hooker_t = int (*)(int (*)(int, int), xy_param &);
using xy_function_t = int (*)(int, int);

auto main(int argc, char **argv) -> int {
  std::cout << std::boolalpha;
  snn::events::event gevent;
  xy_param add_param{ 50, 15 }, sub_param{ 50, 34 }, mul_param{ 3, 45 };
  // snn::main::events::event_handler add_handler(add, 34, 56), sub_handler(sub, 100, 45), mul_handler(mul, 12, 13);
  snn::events::event_handler<xy_hooker_t, xy_function_t, xy_param &>
    add_handler(xy_hooker, add, add_param),
    sub_handler(xy_hooker, sub, sub_param),
    mul_handler(xy_hooker, mul, mul_param);
  snn::events::event_handler<std::string(*)(const std::string &), std::string const &> say_hi_handler(say_hi, "Simon Nganga");
  gevent.subscribe_all("math-them"s, &add_handler, &sub_handler, &mul_handler, &say_hi_handler);
  // gevent.subscribe("math-them"s, &say_hi_handler);
  gevent.emit("math-them"s);
  std::cout << "Add Result: " << add_handler.get_result() << '\n';
  if (say_hi_handler.has_result())
    std::cout << "SayHi Result: " << say_hi_handler.get_result() << '\n';
  else
    std::cout << "SayHi Has No Result\n";
  // say_hi("Simon Nganga");
}