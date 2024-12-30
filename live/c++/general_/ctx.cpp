#include <iostream>
#include <functional>

using Callback = std::function<void()>;
void noop() { }

struct Hello {
  void operator()() const {
    std::cout << "Stop calling me!\n";
  }
  void hey() const {
    std::cout << "Hey from Hello\n";
  }
};

struct Context {
  Context() = delete;
  Context(Callback enter, Callback exit)
  :exit{ exit } { enter(); }
  Context(Callback exit)
  :exit{ exit } { }
  ~Context() { exit(); }
private:
  Callback exit;
};

auto main(int argc, char **argv) -> int {
  Hello *h{ };
  Context _{ [] { std::cout << "Good Morning\n"; }, [] { std::cout << "GoodBye\n"; } };
  Context __{ [&h] { h->operator()(); } };
  h->hey();
  std::cout << "Hello There\n";
}
