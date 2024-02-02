#include <iostream>
#include <concepts>

namespace type {
  template<typename Type, Type Value>
  struct integral_constant {
    static constexpr Type value{ Value };
    using type = Type;
  };
  template<bool value>
  using bool_constant = integral_constant<bool, value>;
  using false_type = bool_constant<false>;
  using true_type = bool_constant<true>;

  template<typename>
  struct is_member_object_ptr : false_type { };

  template<typename Type, typename Class>
  struct is_member_object_ptr<Type Class:: *> : true_type { };

  template<typename Type>
  concept is_member_object_ptr_v = is_member_object_ptr<Type>::value;
}

template<typename Return, typename Class, typename... Args>
Return call_mem(Return(Class:: *member_function)(Args...) const,
  Class const &instance, Args const &...args) {
  return (instance.*member_function)(args...);
}

namespace other {
  struct point {
    int x, y;
    int dot(point const &p) const {
      return x * p.x + y * p.y;
    }
    void operator++() {
      std::cout << "pre-increment operator: void operator++()\n";
    }
    void operator++(int i) {
      std::cout << "post-increment operator: void operator++(int)\n";
    }
  };

  int dot(point const &a, point const &b) {
    std::cout << "other::point\n";
    return a.dot(b);
  }
}

namespace snn {
  struct point {
    int x, y;
  };
  int dot(point const &a, point const &b) {
    std::cout << "snn::point\n";
    return a.x * b.x + a.y + b.y;
  }
}

template<typename Type, typename ...Types>
concept is_one_of_v = (std::same_as<Type, Types> || ...);

template<typename Point> requires is_one_of_v<Point, other::point, snn::point>
std::ostream &operator<<(std::ostream &out, Point const &p) {
  return out << "point(" << p.x << ", " << p.y << ')';
}

#define P(val) std::cout << #val << " = " << val << '\n'

auto main(int argc, char **argv) -> int {
  snn::point a{ 1,2 }, b{ 3,4 };
  std::cout << std::boolalpha;
  std::cout << type::is_member_object_ptr_v<int *> << '\n';
  std::cout << type::is_member_object_ptr_v<decltype(&snn::point::x)> << '\n';

  other::point c{ 5, 6 }, d{ 7,8 };
  dot(a, b);
  dot(c, d);
  P(a);
  P(b);
  P(c);
  P(d);
  /*
  const int age = 21;
  int *age_addr = (int *)&age;
  P(age);
  *age_addr = 30;
  P(age);
  int ptr[]{ 1, 4, 9, 16, 25 };
  int *a = ptr;
  P(*a);
  P(*a++);
  P(*a);
  */
}
