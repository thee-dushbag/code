#include <iostream>
#include <tuple>
#include <string>
#include <iomanip>

struct person {
  std::string name, email;
  unsigned int age : 8;
};

std::ostream& operator<<(std::ostream& out, person const& p) {
  return out << "person(name="
    << std::quoted(p.name)
    << ", email="
    << std::quoted(p.email)
    << ", age="
    << p.age << ")";
}

typedef std::tuple<unsigned char, std::string, std::string> person_t;

auto main(int argc, char** argv) -> int {
  person_t me = { 21, "simongash@gmail.com", "Simon Nganga" };
  person& me2 = (person&)me;
  std::cout << me2 << '\n';
}
