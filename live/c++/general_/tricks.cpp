#include <iostream>
#include <functional>

namespace snn {
  auto from(const char *where) {
    return [=] -> void { std::cout << where << ": Hello There\n"; };
  }
  inline namespace inner {
    std::function hey = snn::from("inner");
  }
  inline namespace outer {
    std::function hello = snn::from("outer");
  }
  struct fused {
    void fun() const && { std::cout << "fused::fun() const &&\n"; }  // Called from rvalue instances
    void fun() const & { std::cout << "fused::fun() const &\n"; } // Called from both lvalue and rvalue in const instances
    void fun() & { std::cout << "fused::fun() &\n"; } // only called from lvalue instances
    void havefun() const { fun(); } // since this is a const member function, the instance is a const &
    void lvalue() & { std::cout << "only called from lvalue instances\n"; }
    void rvalue() && { std::cout << "only called from rvalue instances\n"; }
    void amb() const && { std::cout << "fused::amb() const &&\n"; }
    void amb() const & { std::cout << "fused::amb() const &\n"; }
    void amb() && { std::cout << "fused::amb() &&\n"; }
    void amb() & { std::cout << "fused::amb() &\n"; }
  };

  template<typename Type>
  concept Named = requires { { Type::name } -> std::convertible_to<std::string>; };

  void greet(Named auto const &named) {
    std::cout << "Hello " << std::string(named.name) << ", how was your day?\n";
  }

  template <typename Type>
  void happy_birthday(Type const &aged)
    noexcept requires requires
  { { Type::age } -> std::convertible_to<int>; } {
    std::cout << "Happy birthday, you are now " << int(aged.age) << " years old.\n";
  }

  // Evaluated at compile time
  consteval size_t sum_first_fun(size_t N) {
    size_t s{ 0 };
    for (; N > 0; N--) s += N;
    return s;
  }

  template<const size_t N>
  struct sum_first {
    static constexpr size_t value = N + sum_first<N - 1>::value;
  };

  template<>
  struct sum_first<1> { static constexpr size_t value = 1; };

  template<size_t N>
  constexpr size_t sum_first_v = sum_first<N>::value;

  template <size_t Value>
  struct sequence {
    static constexpr size_t value = Value;
    using next = sequence<value - (value > 0)>;
  };

  template<size_t C, size_t N>
  consteval size_t longcompile() {
    for (size_t s{ 0 }; s < C; ++s)
      sum_first_v<N>;
    return C + N;
  }
}

#ifndef COUNT
# define COUNT 100
#endif

#ifndef SIZE
# define SIZE 1000
#endif

struct named { std::string name; int age; };

auto main(int argc, char **argv) -> int {
  using namespace std::literals;
  snn::fused f;
  f.fun();
  snn::fused().fun();
  snn::fused().havefun();
  f.havefun();
  // snn::fused().lvalue(); // compilation error
  snn::fused().rvalue(); // OKAY
  // f.rvalue(); // compilation error
  f.lvalue(); // OKAY
  const snn::fused c;
  std::cout << "--------------------\n";
  f.amb();
  snn::fused().amb();
  c.amb();
  std::move(c).amb();
  std::cout << "--------------------\n";
  named people[2]{ {"Simon Nganga", 21}, {"Faith Njeri", 11} };
  for (auto &person : people) {
    snn::greet(person);
    snn::happy_birthday(person);
  }
  std::cout << "--------------------\n";
  std::cout << snn::sequence<3>::value << '\n';
  std::cout << snn::sequence<3>::next::value << '\n';
  std::cout << snn::sequence<3>::next::next::value << '\n';
  std::cout << snn::sequence<3>::next::next::next::value << '\n';
  std::cout << snn::sequence<3>::next::next::next::next::value << '\n';
  std::cout << "--------------------\n";
  std::cout << "Template: sum(range(1, " << SIZE << ")) = " << snn::longcompile<COUNT, SIZE>() << '\n';
  std::cout << "Template: sum(range(1, " << SIZE << ")) = " << snn::sum_first_v<SIZE> << '\n';
  std::cout << "Function: sum(range(1, " << SIZE << ")) = " << snn::sum_first_fun(SIZE) << '\n';
}
