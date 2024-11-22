#include <chrono>
#include <cstdlib>
#include <ctime>
#include <exception>
#include <iostream>
#include <string_view>
#include <variant>
#include <vector>

using std::cout;

void *operator new(std::size_t size) {
  cout << "Alloc:  " << size << '\n';
  return std::malloc(size);
}

std::optional<std::string_view> get_name() {
  if(std::rand() > RAND_MAX * 0.5)
    return "Simon Nganga";
  return std::nullopt;
}

template <class... T>
struct type_list;

template <class List, class T>
struct is_one_of;

template <class List, class T>
struct get_index_of;

template <class List, std::size_t I>
struct get_index;

template <class List>
struct get_big;

template <class U, class... T>
struct is_one_of<type_list<T...>, U> {
  constexpr static bool value = (std::is_same_v<U, T> || ...);
};

template <std::size_t I, class U, class H, class... T>
struct _get_index_of {
  constexpr static std::size_t index =
    std::is_same_v<U, H> ? I : _get_index_of<I + 1, U, T...>::index;
};

template <std::size_t I, class U, class H>
struct _get_index_of<I, U, H> {
  constexpr static std::size_t index = std::is_same_v<U, H> ? I : -1;
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
struct get_big<type_list<T...>> : _get_big<0, T...> { };

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

template <std::size_t I, class... T>
struct _destroy;

template <std::size_t I, class H, class... T>
struct _destroy<I, H, T...> {
  static inline void destroy(std::size_t target, void *memory) {
    if(target == I)
      return ((H *)memory)->~H();
    _destroy<I + 1, T...>::destroy(target, memory);
  }
};

template <std::size_t I>
struct _destroy<I> {
  static inline void destroy(std::size_t target, void *memory) { }
};

template <class... T>
struct variant {
  static_assert(sizeof...(T) >= 2, "Variant alternatives must be atleast 2");
  using allowed = type_list<T...>;
  using destroyer = _destroy<0, T...>;
  std::size_t current;
  char memory[get_big<allowed>::size];
  variant(): memory(), current(-1) { }
  template <class U>
    requires is_one_of<allowed, U>::value
  variant(U val): current(get_index_of<allowed, U>::index) {
    *(U *)memory = std::move(val);
  }
  template <class U>
    requires is_one_of<allowed, U>::value
  bool is() const {
    return current == get_index_of<allowed, U>::index;
  }
  bool has_value() const { return current != std::size_t(-1); }
  template <class U>
    requires is_one_of<allowed, U>::value
  U get() const {
    if(is<U>())
      return *(U *)memory;
    throw bad_variant_access();
  }
  void destroy() { destroyer::destroy(current, memory); }
  template <class U>
    requires is_one_of<allowed, U>::value
  variant &operator=(U val) {
    destroy();
    *(U *)memory = std::move(val);
    current = get_index_of<allowed, U>::index;
    return *this;
  }
  ~variant() { destroy(); }
};

struct Object {
  Object() { std::cout << "Object(init)\n"; }
  ~Object() { std::cout << "Object(term)\n"; }
};

std::ostream &operator<<(std::ostream &out, Object const &o) {
  return out << "Object(print)";
}

#define TEST(expr)                                                             \
  do                                                                           \
    try {                                                                      \
      (expr);                                                                  \
      std::cout << "Success: " #expr << '\n';                                  \
    } catch(...) {                                                             \
      std::cout << "Failed: " #expr << '\n';                                   \
    }                                                                          \
  while(0)

int main() {
  variant<float, char, double> value;
  TEST(value.get<char>());
  TEST(value.get<float>());
  TEST(value.get<double>());

  variant<int, double, char, Object> v('5');
  std::cout << "Char: " << v.get<char>() << '\n';
  v = 56.78;
  std::cout << "Double: " << v.get<double>() << '\n';
  v = 5052;
  std::cout << "Int: " << v.get<int>() << '\n';
  v = Object();
  std::cout << "Other: " << v.get<Object>() << '\n';
  return 0;
  std::srand(std::time(nullptr));
  auto name = get_name();
  std::cout << name.value_or("[No Name]") << " is a beautiful name.\n";
  for(int i : {1, 2, 3, 4, 5})
    if(auto name = get_name(); name.has_value())
      std::cout << "Your name is " << *name << '\n';
    else
      std::cout << "Name not found!\n";
  return 0;
  std::vector<int> big_vec(500'000'000, 2011), empty;
  cout << "Expect: " << big_vec.size() * 4 << '\n';
  auto begin = std::chrono::high_resolution_clock::now();
  empty = std::move(big_vec); // Copy
  auto lapse = std::chrono::high_resolution_clock::now() - begin;

  auto lapse_seconds = std::chrono::duration<double>(lapse).count();
  cout << lapse_seconds << '\n';
}
