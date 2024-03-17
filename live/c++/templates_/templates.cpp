#include <iostream>
#include <functional>
#include <templates/all.hpp>

#define printx(x) std::cout << #x << " = " << x << '\n'


template<typename T, typename left, typename right>
struct capture {
  capture() = delete;
  capture(std::function<T(left, right)> const& p)
    : p{ p } { }
  std::function<T(left, right)> p;
};

template<typename T, typename left, typename right>
struct capture_left {
  capture_left() = delete;
  capture_left(std::function<T(left, right)> const& p, left&& left_v)
    : p{ p }, left_v{ std::forward<left>(left_v) } { }
  std::function<T(left, right)> p;
  left left_v;
  operator T() { return left_v; }
};

template<typename T, typename left, typename right>
capture_left<T, left, right> operator|(left left_v, capture<T, left, right> capture) {
  return { capture.p, std::forward<left>(left_v) };
}

// template<typename T, typename left, typename right>
// T operator|(capture_left<T, left, right> capture, right&& right_v) {
//   return capture.p(capture.left_v, right_v);
// }

template<typename T, typename left, typename right>
decltype(auto) operator|(capture_left<T, left, right> capture, right right_v) {
  capture.left_v = capture.p(capture.left_v, right_v);
  return capture;
}

template<typename T>
T add(T t1, T t2) {
  std::cout << "Adding: " << t1 << ' ' << t2 << '\n';
  return t1 + t2;
}

template<typename T, typename ...Ts>
decltype(auto) sumall(T t, Ts ...ts) {
  capture infix = std::function(add<T>);
  std::cout << "t=" << t << '\n';
  return (... | (ts | infix));
}

auto main(int argc, char** argv) -> int {
  printx(sumall(1, 2, 3, 4, 5, 6, 7, 8, 9, 10));

  return 0;

  capture infix_add_int = std::function([] (int a, int b) {
    std::cout << a << ", ";
    return b;
  });

  printx(int(55 | infix_add_int | 45 | 50 | 1 | 2 | 3 | 4));

  tmp::print(1, 2, 3, 'a', 'b', 'c', "Hello", "Simon", "Nganga");
  tmp::variable<char> = 90;
  typename tmp::alias<int> var = 89;
  printx((tmp::variable<char> *var));
  printx(tmp::function(90));
  printx(tmp::Class(89).value);
  tmp::print(1, 2, 3);
  // "1 "
  tmp::print(2, 3);
  // "2 "
  tmp::print(3);
  // "3 "
  tmp::print();
  // "\n"
  // "1 2 3\n"
}
