#include <iostream>

namespace _impl {
  template <std::size_t P, std::size_t D> struct is_prime {
    static constexpr bool value = (P % D != 0) && is_prime<P, D - 1>::value;
  };
  
  template <std::size_t P> struct is_prime<P, 2UL> {
    static constexpr bool value = P % 2 != 0;
  };
} // namespace _impl

template <std::size_t P> struct is_prime : _impl::is_prime<P, P / 2> {};

template <> struct is_prime<0> {
  enum { value = false };
};
template <> struct is_prime<1> {
  enum { value = false };
};
template <> struct is_prime<2> {
  enum { value = true };
};
template <> struct is_prime<3> {
  enum { value = true };
};

template <std::size_t P> constexpr bool is_prime_v = is_prime<P>::value;

#define pexpr(expr) std::cout << #expr << " = " << (expr) << '\n'

int main(int, char **) {
  std::cout << std::boolalpha;
  pexpr(is_prime_v<13>);
  pexpr(is_prime_v<10>);
  pexpr(is_prime_v<23>);
  pexpr(is_prime_v<100>);
  pexpr(is_prime_v<127>);
  pexpr(is_prime_v<239>);
  int value{};
  std::cout << "Age: ";
  std::cin >> value;
  std::cout << "Hey, you are " << value << " years old.\n";
}
