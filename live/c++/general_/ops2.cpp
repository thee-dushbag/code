#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

namespace snn {
  template<typename T, typename... Ts>
  struct is_one_of
    : std::bool_constant<(std::is_same_v<T, Ts> || ...)> { };

  template<typename T, typename... Ts>
  constexpr bool is_one_of_v = is_one_of<T, Ts...>::value;
}

struct point_t {
  std::string name;
  uint point;
  point_t() : name{ }, point{ } { }
  point_t(std::string const &name, uint point)
    : name{ name }, point{ point } { }
  void info() const {
    std::cout << "Info: (point_t): name='" << name << "', point=" << point << '\n';
  }
};

struct person_t {
  std::string name;
  uint age;
  person_t() : name{ }, age{ } { }
  person_t(std::string const &name, uint age)
    : name{ name }, age{ age } { }
  void info() const {
    std::cout << "Info: (person): name='" << name << "', age=" << age << '\n';
  }
};

struct employee_t {
  person_t info;
  std::string email;
  uint salary;
  employee_t() : info{ }, email{ }, salary{ } { }
  employee_t(std::string const &name, std::string const &email, uint age, uint salary)
    : info{ name, age }, email{ email }, salary{ salary } { }
};


template<class T>
concept Named = std::same_as<decltype(T::name), std::string>;

template<class T>
concept Contact = std::same_as<decltype(T::email), std::string>;

template<Contact T>
void contact(T const &obj) {
  std::cout << "Hello " << obj.email << "? Your presence has been requested!\n";
}

template<typename T>
void greet(T const &obj) requires Named<T> {
  std::cout << "Hello " << obj.name << ", how was your day?\n";
}

namespace snn {
  struct inputsrc {
    std::string name;
    uint age;
    inputsrc() : name{ }, age{ } { }
    inputsrc(std::string const &name, uint age)
      : name{ name }, age{ age } { }
    inputsrc &operator>>(std::string &obj) {
      obj = name; return *this;
    }
    inputsrc &operator>>(uint &obj) {
      obj = age; return *this;
    }
    inputsrc &operator<<(std::string const &obj) {
      name = obj; return *this;
    }
    inputsrc &operator<<(uint const &obj) {
      age = obj; return *this;
    }
    inputsrc &operator>>(person_t &p) {
      p = { name, age }; return *this;
    }
    inputsrc &operator<<(person_t const &p) {
      name = p.name; age = p.age; return *this;
    }
    inputsrc &operator<<(employee_t const &e) {
      name = e.info.name; age = e.info.age; return *this;
    }
  };

  inputsrc &getline(inputsrc &isrc, std::string &obj) {
    isrc >> obj; return isrc;
  }
}

snn::inputsrc &operator>>(snn::inputsrc &isrc, point_t &p)
{ p.name = isrc.name; p.point = isrc.age; return isrc; }

snn::inputsrc &operator<<(snn::inputsrc &isrc, point_t const &p)
{ isrc.name = p.name; isrc.age = p.point; return isrc; }

template<class I>
concept IntegerT = snn::is_one_of_v<I, uint, int, long, ulong, unsigned, signed, float>;

auto main(int argc, char **argv) -> int {
  snn::inputsrc isrc;
  // std::stringstream isrc;
  // isrc << "Darius Kimani\n25\n";
  // std::ifstream isrc { "info.txt" };
  isrc << "unit" << 1;
  point_t px;
  isrc >> px;
  greet(px);
  px.info();
  employee_t emp { "Simon Nganga", "simongash@gmail.com", 21, 100000 };
  person_t me;

  isrc << px >> me;
  // isrc.operator<<(emp).operator>>(me);

  greet(me);
  contact(emp);
  me.info();
  // getline(isrc, name);
  // std::cout << "Age: ";
  // isrc >> age;

  // person_t me{ "Simon Nganga", 21 };
  // // contact(me);
  // greet(me);
  // employee_t emp{ "You Lee", "you.lee.chan@gmail.com", 30, 200000 };
  // greet(emp.info);
  // contact(emp);
  // uint x{60}, y{90};
// float a{54.54}, b{36.63};
// auto add = [](IntegerT auto const &x, IntegerT auto const &y) -> IntegerT auto { return x + y; };
// std::cout << "C++: " << x << " + " << y << " = " << add(x, y) << '\n';
// std::cout << "C++: " << a << " + " << b << " = " << add(a, b) << '\n';
}