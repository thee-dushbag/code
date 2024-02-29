#include <iostream>
#include "hi/hi.hpp" // Include the C++ version of hi/hi.h
// Error due to the incorrect use of identifiers class and this
// #include "hi/hi.h"

auto main(int argc, char **argv) -> int {
  std::string name;
  std::cout << "Enter your name: ";
  std::getline(std::cin, name);
  hi::hello(name.c_str());
  int cls;
  std::cout << "Enter a number between -200 to 500: ";
  std::cin >> cls;
  if (cls > 500 or cls < -200) {
    std::cerr << "Expected integer between -200 and 500 inclusive, but got " << cls << '\n';
    return 1;
  }
  std::cout << "You are in " << hi::status(cls) << " CLASS\n";
  std::cout << cls << " * " << cls << " = " << hi::square(cls) << '\n';
}
