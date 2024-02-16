#include <iostream>
#include <snn_pool.hpp>

auto main(int argc, char **argv) -> int {
  auto add = [] (int x, int y) { return x + y; };
  auto mul = [] (int x, int y) { return x * y; };
  // auto t1 = snn::make_task(add, 3, 4);
}
