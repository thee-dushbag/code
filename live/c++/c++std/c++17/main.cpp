#include "string.hpp"
#include <iostream>
#include <map>
#include <string>
#include <type_traits>
#include <unordered_map>
#include <utility>
#include <vector>

struct Thing {
  Thing() { std::cout << "Default: " << this << '\n'; }
  Thing(Thing const &) = delete;
  Thing &operator=(Thing const &) = delete;
  Thing(Thing &&) = delete;
  Thing &operator=(Thing &&) = delete;
  ~Thing() { std::cout << "Destroy: " << this << '\n'; }
};

struct Thing2 {
  int age;
  std::string name;
  bool operator<(Thing2 const &) const { return age; }
  bool operator==(Thing2 const &) const { return age; }
};

template <>
struct std::hash<Thing2> {
  std::size_t operator()(Thing2 const &t) const {
    std::cout << "Hashing: " << t.name << " with age " << t.age << '\n';
    return t.age;
  }
};

struct Value {
  int value;
  static int counter;
  Value(): value(counter++) { std::cout << "DefaultValue: " << value << '\n'; }
  Value(int x): value(x) { std::cout << "IntValue: " << value << '\n'; }
  Value(Value const &v): value(v.value) {
    std::cout << "CopyValue: " << v.value << '\n';
  }
  Value(Value &&v): value(v.value) {
    std::cout << "MoveValue: " << v.value << '\n';
    v.value = 0;
  }
  Value &operator=(Value const &v) {
    std::cout << "CopyAssignValue: " << v.value << '\n';
    value = v.value;
    return *this;
  }
  Value &operator=(Value &&v) {
    std::cout << "MoveAssignValue: " << v.value << '\n';
    value = v.value;
    v.value = 0;
    return *this;
  }
  ~Value() { std::cout << "DestroyValue: " << value << '\n'; }
};

int Value::counter = 1;

template <typename T, std::size_t N>
class Array {
  T payload[N];

public:
  Array() = default;
  constexpr Array(std::initializer_list<T> values)
    requires std::is_copy_constructible_v<T>
  {
    if(values.size() > N)
      throw "TooManyItems";

    auto memory = payload;
    for(auto &&val : values) {
      memory++->~T();
      ::new(memory) T(std::move(const_cast<T &>(val)));
    }
  }
};

int main() {
  Array<Value, 3> values{{4}, {5}, {6}};
  return 0;
  std::initializer_list<string> names = {"Faith", "Njeri", "Wanjiru"};
  /*Array<string, 3> people{"Simon Nganga"};*/
  auto others = names;
  Array<string, 3> one{names};
  std::cout << "Use Array<string>\n";
  for(auto &other : others)
    std::cout << "Other: " << other << '\n';
  std::cout << "Use Array<string>\n";
  return 0;
  std::hash<std::string> hasher;
  std::vector<Thing> things;
  Thing *thing = (Thing *)std::malloc(1);
  std::cout << "thing =  " << thing << '\n';
  ::new(thing) Thing();
  std::cout << "Use thing: " << thing << '\n';
  thing->~Thing();

  std::map<Thing2, int> indexed_things;
  indexed_things[{21, "Simon"}] = 56;
  std::unordered_map<Thing2, int> indexed_things2;
  indexed_things2[{11, "Faith"}] = 23;

  std::vector<int> vec = {1, 2, 3, 4, 5, 6, 7, 8, 9};
  std::vector steal = std::move(vec);
  /*vec.clear();*/

  std::unordered_map<std::string, int> upeople{
    {"Simon", 21}, {"Faith", 11}, {"Lydia", 39}};

  std::cout << "steal.max_size() = " << steal.max_size() << '\n';

  std::map<std::string, int> opeople{upeople.begin(), upeople.end()};
  /*upeople.clear();*/
  for(auto const &data : upeople)
    std::cout << "Hello " << data.first << ", you are " << data.second
              << " years old.\n";

  for(auto const &[name, age] : opeople)
    std::cout << "Hello " << name << ", you are " << age << " years old.\n";

  for(auto number : vec)
    std::cout << number << " * " << number << " = " << number * number << '\n';

  return 0;
}
