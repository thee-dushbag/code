#include <iostream>

struct Value {
  int value;
  Value() : value{ } { }
  Value(int v) : value{ v } { }
  Value &operator++(int) {
    value++;
    return *this;
  }
  Value  &operator++() {
    value++;
    return *this;
  }
  Value &operator*() {
    value++;
    return *this;
  }
  Value &operator+() {
    value++;
    return *this;
  }
  Value &operator+(Value const &) {
    return *this;
  }
};

auto main(int argc, char **argv) -> int {
  Value v{ 5 };
  v++  +  +v++;
  v++;
  ++v;
  ++v++;
  *v++;
}
