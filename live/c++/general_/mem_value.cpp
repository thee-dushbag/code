#include <iostream>
#include <iomanip>
#include <string>
#include <concepts>
#include "live/c++/mem_fn.hpp"

namespace hey {
  struct email {
    std::string val;
    email(std::string const& v)
      : val{ v } { }
    email(std::string&& v)
      : val{ std::move(v) } { }
    email(email&& n)
      : val{ std::move(n.val) } { }
    email(email const& n)
      : val{ n.val } { }
    operator std::string()
      const noexcept {
      return val;
    }
    void operator=(email&& n) noexcept {
      val = std::move(n.val);
    }
    void operator=(email const& n)
      noexcept {
      val = n.val;
    }
    void operator=(std::string&& n) noexcept {
      val = std::move(n);
    }
    void operator=(std::string const& n)
      noexcept {
      val = n;
    }
  };

  std::ostream&
    operator<<(std::ostream& out, email const& n) {
    return out << "email(" << std::quoted(n.val) << ')';
  }

  void swap(email& n1, email& n2) {
    email tmp{ std::move(n1) };
    n1 = std::move(n2);
    n2 = std::move(tmp);
  }

  void hello(email const& n) {
    std::cout << "To " << n.val << ": How are you?\n";
  }
}

namespace snn {
  struct name {
    std::string val;
    name(std::string const& v)
      : val{ v } { }
    name(std::string&& v)
      : val{ std::move(v) } { }
    name(name&& n)
      : val{ std::move(n.val) } { }
    name(name const& n)
      : val{ n.val } { }
    operator std::string()
      const noexcept {
      return val;
    }
    void operator=(name&& n) noexcept {
      val = std::move(n.val);
    }
    void operator=(name const& n)
      noexcept {
      val = n.val;
    }
    void operator=(std::string&& n) noexcept {
      val = std::move(n);
    }
    void operator=(std::string const& n)
      noexcept {
      val = n;
    }
    void greet() {
      std::cout << "Hello " << val
        << ", how was your fucking day?\n";
    }
    std::string hi(name const& o) {
      return (std::stringstream()
        << "Hello " << o.val <<
        ", my name is " << val << '.').str();
    }
  };

  std::ostream&
    operator<<(std::ostream& out, name const& n) {
    return out << "name(" << std::quoted(n.val) << ')';
  }

  void swap(name& n1, name& n2) {
    name tmp{ std::move(n1) };
    n1 = std::move(n2);
    n2 = std::move(tmp);
  }

  void hello(name const& n) {
    std::cout << "Hello " << n.val << "?\n";
  }
}

namespace ev {
  template<typename T>
  concept valued = std::is_same_v<decltype(T::val), std::string>;

  void show_value(valued auto const& v) {
    std::cout << "Value is: " << std::quoted(v.val) << '\n';
  }
}

template <typename Type>
concept NonVoid = not std::same_as<Type, void>;

template<NonVoid _Type, NonVoid _Class>
using member_t = _Type(_Class::*);

template<NonVoid _Type, NonVoid _Class>
struct _Member_value {
  using value_type = _Type;
  using member_class_ptr = _Class;
  using member_type = member_t<_Type, _Class>;

  member_type member;

  _Member_value() = delete;
  _Member_value(member_type&& val)
    : member{ std::forward<member_type>(val) } { }

  decltype(auto)
  get(_Class const& obj) const
  { return obj.*member; }

  decltype(auto)
  operator()(_Class const& obj) const
  { return get(obj); }

  template<NonVoid _Return>
  _Return to(_Class const &obj) const
  requires std::convertible_to<_Type, _Return>
  { return get(obj); }
};

template <NonVoid _Type, NonVoid _Class>
_Member_value<_Type, _Class>
member(member_t<_Type, _Class> mem)
{ return mem; }


auto main(int argc, char** argv) -> int {
  using snn::functional::mem_fn;
  snn::name me{ "Simon Nganga" }, sis{ "Faith Njeri" };
  hey::email mine{ "simongash@gmail.com" };
  // me.greet();
  // void (snn::name:: * sayhi)() const = &snn::name::greet;
  // (me.*sayhi)();

  // std::string(snn::name:: * hello)(snn::name const&) const = &snn::name::hi;

  // std::cout << (me.*hello)(sis) << '\n'
  //   << (sis.*hello)(me) << '\n';

  // auto hi = mem_fn(&snn::name::hi);
  // auto greet = mem_fn(&snn::name::greet);
  // greet(me);
  // greet(sis);
  // std::cout << hi(me, sis) << '\n' << hi(sis, me) << '\n';
  // ev::show_value(me);
  // ev::show_value(mine);
  auto val = member(&snn::name::val);
  std::cout << "Value is: " << val.to<std::string>(me) << '\n';
}