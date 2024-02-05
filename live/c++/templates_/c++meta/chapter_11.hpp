#ifndef _CPP_TEMPLATES_11_
#define _CPP_TEMPLATES_11_

#include <functional>
#include <string>
#include <iostream>
#include <vector>
#include <utility>
#include <snn_type_list.hpp>

namespace temp {
  template<typename Iter, typename Callable>
  void foreach(Iter current, Iter end, Callable op) {
    for (; current != end; ++current) op(*current);
  }

  template <typename Iter, typename Callable, typename ...Args>
  void foreachi(Iter current, Iter end, Callable op, Args const &...args) {
    for (; current != end; ++current) std::invoke(op, args..., *current);
  }

  template<typename Callable, typename ...Args>
  decltype(auto) perfect_return(Callable op, Args ...args) {
    return std::invoke(op, args...);
  }

  namespace utils {
    namespace __detail {
      using namespace snn::list;
      using string_types = typelist<std::string, const char *, std::string_view>;

      template<typename type>
      concept string = is_one_of<type, string_types>::value;

      template<typename T>
      void print(T const &t) {
        std::cout << t;
      }

      void print(string auto const &str) {
        std::cout << '"' << str << '"';
      }

      void print(char const &ch) {
        std::cout << '\'' << ch << '\'';
      }
    }
    template<typename ...Types>
    void print(Types const &...);

    template<typename Type, typename ...Types>
    void print(Type const &arg, Types const &...args) {
      __detail::print(arg);
      std::cout << (sizeof...(Types) ? ", " : "");
      print<Types...>(args...);
    }

    template<>
    void print() {
      std::cout << '\n';
    }
  }
}


template<bool, typename Type = void>
struct enable_if;

template <typename Type>
struct enable_if<true, Type> {
  using type = Type;
};

template<typename T>
void noint(T const &t) {
  std::cout << "NotInt: " << t << '\n';
}

void noint(int const &) = delete;

template<typename T, typename = enable_if<not std::is_same_v<T, int>>::type>
void isint(T const &t) {
  std::cout << "Not Integer: " << t << '\n';
}

void isint(...) {
  std::cout << "Cannot process an integer\n";
}

struct A {
  void a() const {
    std::cout << "Hello\n";
  }
  A &ref() {
    return *this;
  }
};

struct French {
  void hello() const {
    std::cout << "Hola Mundo!!!\n";
  }
  void thanks(std::string const &name) const {
    std::cout << "Gracious " << name << "!\n";
  }
};

namespace mainns {
  namespace _t = temp;
  namespace _u = _t::utils;

  template<typename Bound>
  void call_bound(Bound bound) {
    std::cout << "............setup\n";
    bound();
    std::cout << "............teardown\n";
  }

  template<typename Class, typename ...Args>
  struct Bind {
    typedef void (Class:: *MemberFunction)(Args...) const;

    Bind(MemberFunction member_function, Class const &instance)
      : instance{ instance }, member_function{ member_function } { }
    void operator()(Args ...args) const {
      (instance.*member_function)(std::forward<Args>(args)...);
    }
  private:
    Class instance;
    MemberFunction member_function;
  };

  using number_type = _u::__detail::typelist<int, float, double, char>;

  template<typename T>
    requires _u::__detail::is_one_of<T, number_type>::value
  T multiply(T a, T b) {
    return a * b;
  }

  auto main(int argc, char **argv) -> int {
    multiply(5, 6);
    const char *data = "Hey";
    _u::print("Hello", 1, 2, 3, "Nganga", 'A', std::string{ "Hello World" }, data);

    noint('a');
    noint("Hello");
    noint(56.7f);
    // noint(90); // Fail


    isint("Hello World");
    isint(56);

    A temp;
    decltype(auto) a = _t::perfect_return(&A::ref, temp); // Perfect Capture

    A values[]{ {}, {}, {}, {} };
    _t::foreachi(values, values + 4, &A::a);
    _t::foreachi(values, values + 4, std::mem_fn(&A::a));
    French sister;
    auto others = { "Simon", "Nganga", "Lydia", "Wanjiru" };
    _t::foreachi(others.begin(), others.end(), &French::thanks, sister);

    A a;
    Bind bound{ &A::a, a };
    call_bound(bound);
    call_bound<Bind<French>>({ &French::hello, French{ } });
    Bind thanks{ &French::thanks, sister };
    for (auto name : std::initializer_list<std::string>{ "Simon", "Nganga", "Lydia", "Wanjiru" })
      thanks(name);

    std::vector<int> primes{ 2, 3, 5, 7, 11, 13, 17, 19 };
    // temp::foreach(primes.begin(), primes.end(), _u::print<int>);
  }
}

#endif //_CPP_TEMPLATES_11_