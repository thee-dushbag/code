#include <string_view>
#include <iostream>
#include <string>

struct Point { double x, y; };

std::ostream &operator<<(std::ostream &out, Point const &p)
{ return out << "Point(x=" << p.x << ", y=" << p.y << ')'; }

void hello(std::string_view name) {
  std::cout << "Hello " << name << ", how was your day?\n";
}

auto main(int argc, char **argv) -> int {
  Point x{ .x = 2, .y = 90 };
  hello("Simon Nganga");
  std::cout << x << '\n';
}
