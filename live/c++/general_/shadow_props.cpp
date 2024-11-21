#include <iostream>

struct Base {
  int base;
};

struct Left : Base {
  int one;
  Left(int base, int one) : Base{base}, one{one} {}
};

struct Right : Base {
  int one;
  Right(int base, int one) : Base{base}, one{one} {}
};

struct Thing : Left, Right {
  int thing;
  Thing(int base, int left_one, int right_one, int thing)
      : Left{base, left_one}, Right{base, right_one}, thing{thing} {}
};

std::ostream &operator<<(std::ostream &out, Base const &b) {
  return out << "Base { base: " << b.base << " }";
}
std::ostream &operator<<(std::ostream &out, Left const &b) {
  return out << "Left { base: " << (Base &)b << ", one: " << b.one << " }";
}
std::ostream &operator<<(std::ostream &out, Right const &b) {
  return out << "Right { base: " << (Base &)b << ", one: " << b.one << " }";
}
std::ostream &operator<<(std::ostream &out, Thing const &b) {
  return out << "Thing { left: " << (Left &)b << ", right: " << (Right &)b
             << ", thing: " << b.thing << " }";
}

int main() {
  Thing thing{2, 4, 6, 8};
  thing.thing = 9876543;
  thing.Left::one = 123;
  thing.Right::one = 456;
  thing.Left::base = 789;
  thing.Right::base = 8765;
  Base &left_base = (Left&)thing;
  Base &right_base = (Right&)thing;
  left_base.base = 9000000;
  right_base.base = 33333333;
  std::cout << thing << '\n';
}
