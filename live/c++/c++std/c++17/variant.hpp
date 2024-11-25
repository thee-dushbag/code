#pragma once

#include <cstddef>
#include <exception>
#include <utility>

template <class T, class U>
struct is_same {
  static constexpr bool value = false;
};

template <class T>
struct is_same<T, T> {
  static constexpr bool value = true;
};

template <class T, class U>
constexpr bool is_same_v = is_same<T, U>::value;

template <class... T>
struct type_list;

template <class List, class T>
struct is_one_of;

template <class List, class T>
struct get_index_of;

template <class List, std::size_t I>
struct get_index;

template <class List>
struct get_bigest;

template <class U, class... T>
struct is_one_of<type_list<T...>, U> {
  static constexpr bool value = (is_same_v<U, T> || ...);
};

template <std::size_t I, class U, class H, class... T>
struct _get_index_of {
  constexpr static std::size_t index =
    is_same_v<U, H> ? I : _get_index_of<I + 1, U, T...>::index;
};

template <std::size_t I, class U, class H>
struct _get_index_of<I, U, H> {
  constexpr static std::size_t index = is_same_v<U, H> ? I : -1;
};

template <class U, class... T>
struct get_index_of<type_list<T...>, U> : _get_index_of<0, U, T...> { };

template <std::size_t S, class... T>
struct _get_big;

template <std::size_t S, class H, class... T>
struct _get_big<S, H, T...> {
  constexpr static std::size_t size =
    _get_big<(S > sizeof(H) ? S : sizeof(H)), T...>::size;
};

template <std::size_t S>
struct _get_big<S> {
  constexpr static std::size_t size = S;
};

template <class... T>
struct get_bigest<type_list<T...>> : _get_big<0, T...> { };

template <std::size_t I, class H, class... T>
struct _get_index : _get_index<I - 1, T...> { };

template <class H, class... T>
struct _get_index<0, H, T...> {
  using type = H;
};

template <std::size_t I, class... T>
struct get_index<type_list<T...>, I> : _get_index<I, T...> { };

struct bad_variant_access : std::exception {
  const char *what() const noexcept override { return "BadVariantAccess"; }
};

struct empty_variant : std::exception {
  const char *what() const noexcept override { return "VisitedEmptyVariant"; }
};

template <std::size_t I, class... T>
struct _variant_utils;

template <std::size_t I, class H, class... T>
struct _variant_utils<I, H, T...> {
  static inline void destroy(std::size_t target, void *memory) {
    if(target == I)
      return ((H *)memory)->~H();
    _variant_utils<I + 1, T...>::destroy(target, memory);
  }

  static inline void copy(std::size_t target, void *dest, void *source) {
    if(target == I)
      *((H *)dest) = *((H const *)source);
    _variant_utils<I + 1, T...>::copy(target, dest, source);
  }

  static inline void move(std::size_t target, void *dest, void *source) {
    if(target == I)
      *((H *)dest) = std::move(*((H *)source));
    _variant_utils<I + 1, T...>::move(target, dest, source);
  }

  template <class... Visitor>
  static inline void visit(std::size_t target, void *memory,
                           Visitor &&...visitor) {
    if(target == I)
      return ((void)visitor(*(H *)memory), ...);
    _variant_utils<I + 1, T...>::visit(target, memory,
                                       std::forward<Visitor>(visitor)...);
  }
};

template <std::size_t I>
struct _variant_utils<I> {
  static inline void destroy(std::size_t target, void *memory) { }
  static inline void copy(std::size_t target, void *dest, void *source) { }
  static inline void move(std::size_t target, void *dest, void *source) { }

  template <class... Visitor>
  static inline void visit(std::size_t target, void *memory,
                           Visitor &&...visitor) {
    std::unreachable();
  }
};

template <class T, class List>
concept is_allowed = is_one_of<List, T>::value;

template <class T, class... Ts>
struct variant {
  using allowed = type_list<T, Ts...>;
  using utils = _variant_utils<0, T, Ts...>;
  template <class U>
  using index_of = get_index_of<allowed, U>;

  std::size_t current;
  char memory[get_bigest<allowed>::size];

  variant(): memory(), current(-1) { }
  bool has_value() const { return current != std::size_t(-1); }
  ~variant() { utils::destroy(current, memory); }

  variant(variant const &v): current(v.current) {
    utils::copy(current, memory, v.memory);
  }

  variant(variant &&v): current(v.current) {
    utils::move(current, memory, v.memory);
  }

  template <is_allowed<allowed> U>
  variant(U val): current(index_of<U>::index) {
    *(U *)memory = std::move(val);
  }

  template <is_allowed<allowed> U, class... Args>
  void emplace(Args &&...args) {
    utils::destroy(current, memory);
    current = index_of<U>::index;
    ::new(memory) U(args...);
  }

  template <is_allowed<allowed> U>
  bool is() const {
    return current == index_of<U>::index;
  }

  template <is_allowed<allowed> U>
  U &get() const {
    if(is<U>())
      return *(U *)memory;
    throw bad_variant_access();
  }

  template <is_allowed<allowed> U>
  variant &operator=(U val) {
    utils::destroy(current, memory);
    *(U *)memory = std::move(val);
    current = index_of<U>::index;
    return *this;
  }

  void destroy() {
    utils::destroy(current, memory);
    current = -1;
  }
};

template <class Visitor, class... Visitors, class... T>
void visit(variant<T...> const &v, Visitor &&visitor, Visitors &&...visitors) {
  if(v.has_value())
    return variant<T...>::utils::visit(v.current, (void *)v.memory,
                                       std::forward<Visitor>(visitor),
                                       std::forward<Visitors>(visitors)...);
  throw empty_variant();
}
