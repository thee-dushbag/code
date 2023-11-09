#include <iostream>
#include <iomanip>
#include <vector>
#include <variant>
#include <algorithm>

/*
Ilustration of ADL
  A - Argument
  D - Dependency
  L - Lookup
C++ Feature
*/

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

auto main(int argc, char** argv) -> int {
  snn::name sis{ "Simon Nganga" }, me{ "Faith Njeri" };
  std::cout << "Me: " << me << " | Addr: " << (void*)std::addressof(me.val.front()) << '\n';
  std::cout << "Sis: " << sis << " | Addr: " << (void*)std::addressof(sis.val.front()) << '\n';
  hello(me); // Found using ADL since the argument comes from snn namespace hence hello found in snn
  swap(me, sis); // Similar to that of hello
  std::cout << "Me: " << me << " | Addr: " << (void*)std::addressof(me.val.front()) << '\n';
  std::cout << "Sis: " << sis << " | Addr: " << (void*)std::addressof(sis.val.front()) << '\n';

  hey::email mine{ "simongash@gmail.com" }, mum{ "lydiawanjiru@yahoo.com" };
  std::vector<std::variant<snn::name, hey::email>> values{ sis, mine, mum, me };

  std::for_each(
    std::begin(values),
    std::end(values),
    /*
    Without ADL, the visitor lambda would need two overloaded
    implementations for snn::name and hey::email but due to ADL,
    depending on the value of val on the current passed variant value,
    the correct hello is dispatched.
    */
    [](auto& value) {
      std::visit([](auto& val) {
        std::cout << "Value: " << val.val << " | ";
        hello(val);
        },
        value);
    }
  );
}