#include <iostream>
#include <string>

namespace snn {
  enum class type : char {
    neutral,
    negative,
    positive
  };

  const char *to_string(type const &t) noexcept {
    using enum type;
    switch (t)
    {
#define __case_t(TYPE) case TYPE: return #TYPE
      __case_t(neutral);
      __case_t(positive);
      __case_t(negative);
      default: return "<unknown>";
#undef __case_t
    }
  }

  struct state {
    state() noexcept : value{ type::neutral } { }
    state(type const &value) noexcept : value{ value } { }
    operator std::string() const noexcept {
      std::string str{ "state(" };
      str += to_string(value);
      str.push_back(')');
      return str;
    }
    state operator-() const {
      return { type::negative };
    }
    state operator+() const {
      return { type::positive };
    }
  private:
    type value;
  };

  std::ostream &operator<<(std::ostream &out, state const &s) {
    return out << std::string(s);
  }
}

#define PRINT(val) std::cout << #val << " = " << val << '\n'

auto main(int argc, char **argv) -> int {
  snn::state s;
  PRINT(s);
  PRINT(-s);
  PRINT(+s);
}

#undef PRINT
