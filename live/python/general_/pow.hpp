#ifndef __POW_IMPL_IN_CPP
#define __POW_IMPL_IN_CPP

#include <cmath>
#include <span>
#include <iostream>
#include <limits>

#ifdef SNN_VERBOSE
# define _SNN_VERBOSE 1
#else
# define _SNN_VERBOSE 0
#endif

namespace snn {
  void hello() {
    std::cout << "Hello World\n";
  }

  int sum(int x, int y) {
    std::cout << x << " + " << y << " = " << (x + y) << '\n';
    return x + y;
  }

  struct ExpBaseTracker {
    long double base;
    uint exp;
    ExpBaseTracker()
      : base{ }, exp{ } { }
    ExpBaseTracker(long double b, uint e)
      : base{ b }, exp{ e } { }
  };

  std::ostream &operator<<(std::ostream &out, ExpBaseTracker const &tracker) {
    return out << "{base: " << tracker.base << ", exp: " << tracker.exp << '}';
  }

#ifndef _GLIBCXXSPAN
  std::ostream &operator<<(std::ostream &out, std::span<ExpBaseTracker> const &tracker_arr) {
    std::size_t len{ tracker_arr.size() }, counter{ 1 };
    out << '[';
    for (ExpBaseTracker const &tracker : tracker_arr) {
      out << tracker;
      if (counter < len)
        out << ", ";
      ++counter;
    }
    return out << ']';
  }
#endif

  long double pow(long double base, long e) {
    if (base == 0) return 0;
    if (e == 0) return 1;
    if (std::abs(base) == 1)
      return (e & 1) ? base : std::abs(base);
    long long exp = e;
    if (exp < 0) {
      if (exp == std::numeric_limits<long>::min() and std::abs(base) < 1)
        return 0;
      exp = -exp;
      base = 1 / base;
    }
    if (exp == 1) return base;
    if (exp == 2) return base * base;

    uint exp_decay{ 1 };
    u_short rounds = std::floor(std::log2(exp));
    ExpBaseTracker cache[rounds];
    long double temp{ base };
    base = 1;

    for (int round = 0; round < rounds; ++round) {
      base *= temp;
      temp *= temp;
      exp_decay *= 2;
      cache[round] = { base, exp_decay - 1 };
    }

#if _SNN_VERBOSE
    std::cout << "cache=" << std::span{ cache, cache + rounds } << '\n';
#endif

    exp -= cache[rounds - 1].exp;
    temp = cache[0].base;

    while (exp > 1) {
      rounds = std::floor(std::log2(exp));
#if _SNN_VERBOSE
      std::cout << "exp=" << exp << " rounds=" << rounds << '\n';
#endif
      temp *= cache[rounds - 1].base;
      exp -= cache[rounds - 1].exp;
    }

    return base * temp;
  }
}

#endif //__POW_IMPL_IN_CPP