#include <iostream>
#include <numeric>
#include <vector>
#include <algorithm>
#include <cassert>

#define print(E) std::cout << #E << " = " << (E) << '\n'
template<typename A, typename B>
std::ostream& operator<<(std::ostream& out, std::pair<A, B> const& pair) {
  return out << "{ " << pair.first << ", " << pair.second << " }";
}

using digits = std::vector<int>; // std::vector<One of [0123456789]>

std::ostream& operator<<(std::ostream& out, digits const& d) {
  for ( auto g : d ) out << g;
  return out;
}

template<class T>
decltype(auto) minmax(T const& a, T const& b) {
  return b > a ? std::pair(a, b) : std::pair(b, a);
}

#ifndef NS
# define NS
#endif

digits add(digits a, digits b) {
  std::reverse(a.begin(), a.end());
  std::reverse(b.begin(), b.end());
  auto min_len = std::min(a.size(), b.size());
  auto max_len = std::max(a.size(), b.size());
  digits r;
  digits::value_type arg, over = 0;
  for ( int idx = 0; idx < min_len; idx++ ) {
    arg = a[idx] + b[idx] + over;
    over = int(arg / 10); arg %= 10;
    r.push_back(arg);
  }
  if ( max_len != min_len ) {
    digits const& l = a.size() > b.size() ? a : b;
    for ( int idx = min_len; idx < max_len; idx++ ) {
      arg = l[idx] + over;
      over = int(arg / 10); arg %= 10;
      r.push_back(arg);
    }
  }
  if ( over ) r.push_back(over);
  std::reverse(r.begin(), r.end());
  return r;
}

digits multiply(digits a, digits b) {
  std::vector<digits> rs;
  digits::value_type arg, over = 0;
  digits::reverse_iterator rb, ra;
  for ( rb = b.rbegin(); rb != b.rend(); rb++ ) {
    rs.push_back({ });
    for ( ra = a.rbegin(); ra != a.rend(); ra++ ) {
      arg = *rb * *ra + over;
      over = int(arg / 10); arg %= 10;
      rs.back().push_back(arg);
    }
    if ( over ) rs.back().push_back(over);
    std::reverse(rs.back().begin(), rs.back().end());
    over = 0;
  }
  for ( int idx = 0; idx < rs.size(); idx++ )
    for ( int i = 0; i < idx; i++ )
      rs[idx].push_back(0);
  return std::reduce(rs.begin(), rs.end(), digits{ 0 }, add);
}

digits power(digits a, int b) {
  digits c = a;
  for ( ; b > 0; b-- ) a = multiply(a, c);
  return a;
}

digits todig(u_int64_t d) {
  digits r;
  while ( d ) {
    r.push_back(d % 10);
    d /= 10;
  }
  if ( r.empty() ) r.push_back(0);
  else std::reverse(r.begin(), r.end());
  return r;
}

struct uint128_t {
  u_int64_t bits[2];
  uint128_t()
    :bits{ 0, 0 } { }
  uint128_t(u_int64_t val)
    :bits{ val, 0 } { }
  uint128_t(uint128_t const& u)
    : bits{ u.bits[0], u.bits[1] } { }
  uint128_t operator+(u_int64_t v) {
    u_int64_t left = std::numeric_limits<u_int64_t>::max() - bits[0];
    if ( left >= v )
      return bits[0] + v;
    uint128_t r;
    r.bits[0] = v - left - 1;
    r.bits[1] = bits[1] + 1;
    return r;
  }
  void set_all() {
    bits[0] = bits[1] = 0xff'ff'ff'ff'ff'ff'ff'ff;
  }
};

digits clean(digits a) {
  std::reverse(a.begin(), a.end());
  while ( not a.empty() and a.back() == 0 ) a.pop_back();
  if ( a.empty() ) a.push_back(0);
  else std::reverse(a.begin(), a.end());
  return a;
}

std::ostream& operator<<(std::ostream& out, uint128_t d) {
  return out << clean(
    add(
      todig(d.bits[0]),
      multiply(
        add(
          { 1 },
          todig(std::numeric_limits<u_int64_t>::max())
        ),
        todig(d.bits[1])
      )
    )
  );
}

void test_minmax() {
  size_t low{ 10 }, high{ 20 }, mid{ 15 };
  print(low);
  print(high);
  print(mid);

#define test_func(F)   \
  print(F(low, high)); \
  print(F(low, mid));  \
  print(F(mid, high)); \
  print(F(mid, low));  \
  print(F(high, mid)); \
  print(F(high, low)); \

  test_func(std::min);
  test_func(std::max);
  test_func(std::minmax);

#undef test_func
}

auto main(int argc, char** argv) -> int {
  uint128_t a = std::numeric_limits<u_int64_t>::max();
  print(a);
  a = a + std::numeric_limits<u_int64_t>::max(); // Can handle biggest
  // integer in C++ as per now
  print(a);
  a.set_all(); // Activate all bits in the integer
  // max<uint128>() = 340282366920938463463374607431768211455
  print(a.bits[0]);
  print(a.bits[1]);
  print(a); // Now a == 2 ** 128 - 1
  // Overflow error but not raised, follows 
  // modular arithmetic rules
  print(a + 1); // Back to 0, Overflow.
  return 0;

  digits e{ todig(std::numeric_limits<u_int32_t>::max()) };
  for ( int i = 1; i < 100; i++ ) {
    std::cout << clean(power(e, i)) << '\n';
  }
  // Weird right, we create an extremely powerful
  // integer type, digits, only to help us create
  // a finite integer type that can have overflows
}
