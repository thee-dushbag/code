#include <functional>
#include <iostream>

namespace snn {
  template <class Iter, class Callable>
  void foreach(Iter current, Iter end, Callable && op) {
    while(current != end)
      (void)op(*current++);
  }

  template <std::size_t N, class T, class Callable>
  void foreach(T (&array)[N], Callable && op) {
    foreach(array, array + N, std::forward<Callable>(op))
      ;
  }
} // namespace snn

template <class T>
struct Linear {
  T a, b;
  T operator()(T &x) const {
    x = a * x + b;
    return x;
  }
};

template <class T>
struct Reduce {
  using BinOP = std::function<T(T, T)>;
  T value;
  BinOP op;
  Reduce() = delete;
  Reduce(BinOP &&op, T init): op(op), value(init) { }
  Reduce(BinOP &&op): op(op), value() { }
  void operator()(T const &t) { this->value = this->op(this->value, t); }
};

template <class T>
struct Sinear {
  T scalar;
  Sinear(): scalar(1) { }
  Sinear(T const &t): scalar(t) { }
  T operator()(T const &p, T const &t) const { return scalar * t + p; }
};

int main() {
  int values[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  Linear linear{5, 10};
  snn::foreach(values, linear);
  /*Reduce<int> reducer{[](auto a, auto b) -> auto { return a + b; }};*/
  Sinear scale{7};
  Reduce<int> reducer{scale};
  snn::foreach(values, reducer);
  snn::foreach(values, [] [[nodiscard]] (int v) -> int {
    std::cout << '\t' << v << '\n';
    return v;
  });
  std::cout << "reducer.value: " << reducer.value << '\n';
  int i = 100, j = 200, &a = i;
#define _P(e) (#e " = ") << e << ' '
#define P(e1, e2, e3) std::cout << _P(e1) << _P(e2) << _P(e3) << '\n'
  P(a, i, j);
  a = j;
  P(a, i, j);
  j = 100;
  P(a, i, j);
#undef _P
#undef P
}
