#include <iostream>
#include <string>

template <typename T>
struct Named {
  Named(T const &name)
    : name{ name } { }
  T name;
};

template<typename T>
void print(T const &t) {
  std::cout << t << '\n';
}

template<typename Type, typename ...Types>
concept is_one_of = (std::is_same_v<Type, Types> || ...);

template<typename T>
  requires is_one_of<std::decay_t<T>, const char *, std::string, std::string_view, char *>
void print(T const &str) {
  std::cout << '"' << str << '"' << '\n';
}

void print(char const &ch) {
  std::cout << '\'' << ch << '\'' << '\n';
}

// Template Deduction Guides
template<const size_t N>
Named(char(&)[N]) -> Named<std::string>;
Named(char *)->Named<std::string>;
Named(const char *)->Named<std::string>;


auto main(int argc, char **argv) -> int {
  Named me{ "Hey" };
  print(me.name.c_str());
  print("Hello");
  print(me.name);
  print(90);
  print('A');
}