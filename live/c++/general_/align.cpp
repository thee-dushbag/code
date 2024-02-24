#include <iostream>

struct Zero         {            void plus0(); };
struct One   : Zero { int one;   void plus1(); };
struct Two   : One  { int two;   void plus2(); };
struct Three : Two  { int three; void plus3(); };

// Method definitions are then defined and will be converted as below
void Zero::plus0()  {             }
void One::plus1()   { one   += 1; }
void Two::plus2()   { two   += 1; }
void Three::plus3() { three += 1; }

// On compilation, the above is converted to what is seen below
// The structs remain as simple data blobs
struct _Zero          {            };
struct _One   : _Zero { int one;   };
struct _Two   : _One  { int two;   };
struct _Three : _Two  { int three; };

// For the method declartions, they appear like so
void _Zero_plus0(_Zero  *const);
void _One_plus1(_One   *const);
void _Two_plus2(_Two   *const);
void _Three_plus3(_Three *const);

// `this` is simply the instance passed to the first argument
// as some const pointer to some const/non-const qualified caller
void _Zero_plus0(_Zero  *const _this)  {                    }
void _One_plus1(_One   *const _this)   { _this->one   += 1; }
void _Two_plus2(_Two   *const _this)   { _this->two   += 1; }
void _Three_plus3(_Three *const _this) { _this->three += 1; }

auto main(int argc, char **argv) -> int {
  std::cout << std::boolalpha;
  std::cout <<
    "Zero:  " << sizeof(Zero)  << " | " << // This is EBCO = Empty Base Class Optimization
    "int:   " << sizeof(int)   << " | " <<
    "One:   " << sizeof(One)   << " | " <<
    "Two:   " << sizeof(Two)   << " | " <<
    "Three: " << sizeof(Three) << '\n';

  int data[]{ 10, 20, 30 };
  One *one = (One *)data;
  Two *two = (Two *)data;
  Three *three = (Three *)data;

  one->plus1();
  two->plus2();
  three->plus3();

  // Equivalents. The casts are just for type conformance
  _One_plus1((_One *)one);
  _Two_plus2((_Two *)two);
  _Three_plus3((_Three *)three);

  std::cout <<
    "One::one:     " << one->one     << '\n' <<
    "Two::one:     " << two->one     << '\n' <<
    "Two::two:     " << two->two     << '\n' <<
    "Three::one:   " << three->one   << '\n' <<
    "Three::two:   " << three->two   << '\n' <<
    "Three::three: " << three->three << '\n' <<
    '\n';

  one = (One *)(data + 1);
  two = (Two *)(data + 1);

  std::cout <<
    "One::one:     " << one->one     << '\n' <<
    "Two::one:     " << two->one     << '\n' <<
    "Two::two:     " << two->two     << '\n' <<
    '\n';

  one = (One *)(data + 2);

  std::cout <<
    "One::one:     " << one->one     << '\n' <<
    '\n';

  for (One &one: (One (&)[3])data)
    std::cout << "One::one = " << one.one << '\n';
}
