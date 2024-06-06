#include <iostream>
#include <generator>
#include <ranges>
#include <algorithm>
#include <coroutine>
#include <thread>
#include <chrono>
#include <future>

std::generator<int> range(int start, int stop, int step = 1) {
  while ( start < stop ) {
    co_yield start;
    start += step;
  }
}

struct H {
  int operator co_await() {
    return 45;
  }
};

auto main(int argc, char** argv) -> int {
  std::packaged_task<std::pair<int, int>(int)> sqr{
    [](int a) -> std::pair<int, int> {
    // throw a * a;
    return { a, a * a };
  } };
  std::future fut = sqr.get_future();
  sqr(16);
  sqr.reset();
  try {
    auto&& [base, square] = fut.get();
    std::cout << base << " * " << base << " = " << square << '\n';
  } catch ( std::future_error ) {
    std::cout << "Broken Promise\n";
  } catch ( int result ) {
    std::cout << "What: " << result << '\n';
  }
  auto _1to10 = range(1, 11);
  std::ranges::for_each(_1to10, [] (int v) -> void {
    std::cout << "Value: " << v << '\n';
  });
}
