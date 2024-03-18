#include <iostream>
#include <cstdint>
#include <vector>

struct Valued {
  const short value;
  static short counter;
  static std::vector<Valued> all;
  Valued(): value{ counter++ } { all.push_back(*this); }
  Valued(Valued const& v): value{ v.value } { }
  Valued(Valued&& v): value{ v.value } { }
};

short Valued::counter = 1;
std::vector<Valued> Valued::all{ };

std::ostream& operator<<(std::ostream& out, Valued& v) {
  return out << "V(" << v.value << ')';
}

Valued& operator +(Valued& a, Valued& b) {
  std::cout << a << ' ';
  return a.value > b.value ? a : b;
}

std::ostream& operator<<(std::ostream& out, std::vector<Valued>& all) {
  out << "Valued: ";
  for ( Valued& value : all ) out << value << ' ';
  return out;
}

#define pfold(fold) std::cout << '(' << #fold << "): "; (fold)

template<typename ...T>
void plus_fold_right(T &...ts) { pfold(ts + ...); }

template<typename ...T>
void plus_fold_left(T &...ts) { pfold(... + ts); }

#undef pfold

auto main(int argc, char** argv) -> int {
  Valued i1{ }, i2{ }, i3{ }, i4{ }, i5{ }, i6{ }, i7{ }, i8{ }, i9{ }, i10{ }, i11{ };
  Valued::all.pop_back(); // Loose i11, will not appear in the folds.
  std::cout << Valued::all << '\n';
  plus_fold_right(i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11);
  std::cout << '\n';
  plus_fold_left(i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11);
  std::cout << '\n';
}
