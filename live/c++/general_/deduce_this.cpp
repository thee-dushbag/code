#include <concepts>
#include <iostream>

template <class T>
concept has_name = requires {
  { T::name } -> std::convertible_to<std::string_view>;
};

struct Base {
  const char*name = "Base::name";
  void greet(this auto &&self) {
    std::cout << "Hello " << self.get_name() << ", how is your day?\n";
  }
  const char* get_name() const {
    return "Lydia Njeri";
  }
};

struct Child : Base {
  const char *name;
  const char *get_name() const {
    return name;
  }
};

int main() {
  Base b;
  b.greet();
  Child c{{}, "Simon Nganga"};
  c.greet();
  Base &base = c;
  base.greet();
}
