#include <iostream>

struct Value {
  int value;
  Value() : value{ value } { }
  explicit Value(int value) : value{ value } { }
};

struct A;

struct B : public Value {
  B() : Value{ } { }
  explicit B(int value) : Value{ value } { }
  B operator+(B const &other) const noexcept {
    return B{ value + other.value };
  }
  B operator-(A const &other) const noexcept;
  B operator-(B const &other) const noexcept {
    return B{ value - other.value };
  }
};

struct A : public Value {
  A() : Value{ } { }
  explicit A(int value) : Value{ value } { }
  A operator+(A const &other) const noexcept {
    return A{ value + other.value };
  }
  A operator+(B const &other) const noexcept {
    return A{ value + other.value };
  }
  A operator-(A const &other) const noexcept {
    return A{ value - other.value };
  }
  A operator-(B const &other) const noexcept {
    return A{ value - other.value };
  }
};

struct C : public Value {
  C() : Value{ } { }
  C(int value) : Value{ value } { }
};

B B::operator-(A const &other) const noexcept {
  return B{ value - other.value };
}

Value operator+(Value const &a, Value const &b) {
  return Value{ a.value + b.value };
}

template<class _class>
struct class_name;

#define CLASS_NAME(Type)                        \
  template<>                                    \
  struct class_name<Type> {                     \
    constexpr static const char *name = #Type;  \
    using type = void;                          \
  }

CLASS_NAME(A);
CLASS_NAME(B);
CLASS_NAME(C);
CLASS_NAME(Value);

#undef CLASS_NAME

template<typename _class>
const char *cls_name = class_name<_class>::name;

template<typename Type, typename = typename class_name<Type>::type> // SPHINAE
  requires std::derived_from<Type, Value> or std::same_as<Type, Value> // CONCEPTS
std::ostream &operator<<(std::ostream &out, Type const &inst) noexcept {
  return out << cls_name<Type> << '(' << inst.value << ')';
}

auto main(int argc, char **argv) -> int {
  A a{ 45 };
  B b{ 55 };
  std::cout << a << '\n' << b << '\n';
  a + b;
  std::cout << a << '+' << b << '=' << (a + b) << '\n';
  // b + a;
  std::cout << a << '-' << b << '=' << (a - b) << '\n';
  std::cout << b << '-' << a << '=' << (b - a) << '\n';
  a = a - b;
  b = b - a;
  Value v{ 90 };
  std::cout << v << '\n';
  std::cout << v << '+' << a << '=' << (v + a) << '\n';
  C c{ 23 };
  std::cout << v << '+' << c << '=' << (v + c) << '\n';
  std::cout << c << '+' << v << '=' << (c + v) << '\n';
}
