#include <iostream>

struct One {
  virtual const char *two() const = 0;
  void one() { std::cout << "One::two(this) = " << this->two() << '\n'; }
};

struct Two : One {
  const char *two() const override { return "Simon Nganga"; }
};

template <typename T> struct Three {
  void three() const {
    auto self = static_cast<const T &>(*this);
    std::cout << "Three::four(this) = " << self.four() << '\n';
  }
};

struct Four : Three<Four> {
  const char *four() const { return "Faith Njeri"; }
};

struct Five {
  void five(this auto &&self) {
    std::cout << "Five::five(self) = " << self.six() << '\n';
  }
};

struct Six: Five {
  const char *six() const {
    return "Lydia Njeri";
  }
};

template <typename T> struct Crtp {
  void greet() const {
    auto self = static_cast<const T &>(*this);
    std::cout << "Hi " << self.name << ", I am Crtp::greet()\n";
  }
};

struct Derived : Crtp<Derived> {
  std::string name;
  Derived(std::string const &name) : Crtp{}, name{name} {}
};

struct Base {
  void greet(this auto &&self) {
    std::cout << "Hello " << self.name << " from Base::print(self)\n";
  }
};

struct Child : Base {
  std::string name;
  Child(std::string const &name) : Base{}, name{name} {}
};

struct Object {
  const char *name = "Object";
};

int main() {
  Two two;
  One &one = two;
  one.one();
  Four four;
  Three<Four> &three = four;
  three.three();
  Six six;
  six.five();
  Child me{"Simon Nganga"};
  me.greet();
  Derived d{"Faith Njeri"};
  d.greet();
}
