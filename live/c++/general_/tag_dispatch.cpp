#include <iostream>

// TAG types
struct category_one { };
struct category_two { };
struct category_three { };
struct category_four {
  operator category_three const &() const noexcept;
};

// TAG instants to be used for dispatch
category_one   category_one_tag;
category_two   category_two_tag;
category_three category_three_tag;
category_four category_four_tag;

// Make category four same as category three for hello overloads
category_four::operator
category_three const &()
const noexcept
{ return category_three_tag; }

// For aggregating TAGs
template<typename ...types>
struct typelist;

// For checking if a TAG type is in the TAG aggregate
template<typename type, typename list>
struct is_one_of;

// Implementation of the above
template<typename type, typename ...types>
struct is_one_of<type, typelist<types...>> :
  std::bool_constant<(std::is_same_v<type, types> || ...)> { };

// Syntactic sugar for better error and less typing
template<typename type, typename ...types>
concept is_one_of_v = is_one_of<type, types...>::value;

// Group of valid categories
using categories = typelist<category_one, category_two, category_three, category_four>;

template<typename category>
  requires is_one_of_v<category, categories>
struct Class { void method(); };

template<>
void Class<category_one>::method() {
  std::cout << "Tag: category_one\n";
}

template<>
void Class<category_two>::method() {
  std::cout << "Tag: category_two\n";
}

template<>
void Class<category_three>::method() {
  std::cout << "Tag: category_three\n";
}

template<typename category = category_one>
  requires is_one_of_v<category, categories>
struct Resource {
  Resource(std::string const &name) : name{ name }, tag{ } { }
  Resource(category const &tag) : name{ }, tag{ tag } { }
  Resource(std::string const &name, category const &tag)
    : name{ name }, tag{ tag } { }
  std::string name;
  category const &tag;
};

namespace _impl {
  void hello(std::string const &name, category_one const &) {
    std::cout << "Tag: one | Hello " << name << ", how was your day?\n";
  }
  void hello(std::string const &name, category_two const &) {
    std::cout << "Tag: two | Hello " << name << "?\n";
  }
  void hello(std::string const &name, category_three const &) {
    std::cout << "Tag: three | Ola " << name << "?\n";
  }
  // template<typename any>
  // void hello(std::string const &name, any const &) {
  //   std::cout << "This category is invalid.\n";
  // }
}

template<typename category>
void hello(Resource<category> const &resource) {
  _impl::hello(resource.name, resource.tag);
}

auto main(int argc, char **argv) -> int {
  Class<category_one> one;
  Class<category_two> two;
  Class<category_three> three;
  one.method();
  two.method();
  three.method();
  Resource p1{ "Simon Nganga" };
  Resource p2{ "Faith Njeri", category_two_tag };
  Resource<category_three> p3{ "Lydia Njeri" };
  Resource p4{ "Darius Kimani", category_four_tag };
  hello(p1);
  hello(p2);
  hello(p3);
  hello(p4);
}
