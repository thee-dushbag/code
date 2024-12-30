#pragma once

#include <utility>

namespace snn {
  template <typename>
  struct function;

  template <typename functor_t, typename... args_t>
  decltype(auto) invoke(functor_t functor, args_t &&...args) {
    return functor(std::forward<args_t>(args)...);
  }

  template <typename functor_t, typename... args_t>
  void create(void *memory, args_t &&...args) {
    new(memory) functor_t(std::forward<args_t>(args)...);
  }

  template <typename functor_t>
  void destroy(void *memory) {
    static_cast<functor_t *>(memory)->~functor_t();
  }

  template <typename>
  struct function_base;

  template <typename functor_t, typename... args_t>
  struct function_base<functor_t(args_t...)> {
    using return_t =
      decltype(std::declval<functor_t>()(std::declval<args_t>()...));
  };

  template <typename return_t, typename... args_t>
  struct function<return_t(args_t...)> { };
} // namespace snn
