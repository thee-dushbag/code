#ifndef __CPP_TEMPLATES_HPP
#define __CPP_TEMPLATES_HPP

#include <iostream>
#include "kinds.hpp"

namespace tmp {

  namespace _ {
    template<typename Type>
    void print(Type&& value) {
      std::cout << value;
    }
  }

  template<typename ...T>
  void print(T &&...);

  template<typename T, typename ...Ts>
  void print(T&& t, Ts &&...ts) {
    _::print(std::forward<T>(t));
    _::print(' ');
    print(std::forward<Ts>(ts)...);
  }

  template<>
  void print() { _::print('\n'); }

  void hello() {
    std::cout << "Hello World\n";
  }
}

#endif //__CPP_TEMPLATES_HPP