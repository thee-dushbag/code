#include "string.hpp"
#include "variant.hpp"
#include <ctime>
#include <iostream>

struct person {
  string name;
  int age;
};

std::ostream &operator<<(std::ostream &out, person const &p) {
  return out << "person(name='" << p.name << "', age=" << p.age << ')';
}

variant<string, person> get_value() {
  if(std::rand() > (RAND_MAX * 0.5))
    return person{"Faith Njeri", 11};
  return string("Simon Nganga Njoroge");
}

int main() {
  std::srand(std::time(NULL));
  auto thing = get_value();
  auto other = std::move(thing);
  visit(
    thing, [](auto &&p) { std::cout << "VisitorOne: " << p << '\n'; },
    [](auto &&p) { std::cout << "VisitorTwo: " << p << '\n'; });
  thing.emplace<person>("John Doe", 21);
  struct {
    void operator()(person &p) const {
      std::cout << "Hello " << p.name << ", you are " << p.age
                << " years old.\n";
    }
    void operator()(string &s) const { std::cout << "Hi " << s << "?\n"; }
  } greeter;
  visit(thing, greeter);
  thing.emplace<string>("Anne Monroe");
  visit(thing, greeter);
}
