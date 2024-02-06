#ifndef _SNN_HPP_UTILS_
#define _SNN_HPP_UTILS_

#include <iostream>
#include "sem.hpp"

namespace snn {
  namespace __detail {
    _17::Semaphore _print_lock{ 1 };

    template<typename ...Types>
    void _print_impl(Types const &...args);

    template<typename Type, typename ...Types>
    void _print_impl(Type const &arg, Types const &... args) {
      std::cout << arg;
      _print_impl(args...);
    }

    template<>
    void _print_impl() {
      std::cout << '\n';
    }
  }
  template<typename ...Types>
  void print(Types const &...args) {
    _17::Session _{ __detail::_print_lock };
    __detail::_print_impl(args...);
  }

}

#endif //_SNN_HPP_UTILS_