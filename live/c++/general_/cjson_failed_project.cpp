#include <iostream>
#include <fstream>
#include <cstdint>
#include <variant>
#include <map>
#include <functional>
#include <string>
#include <vector>
#include <strstream>
#include <algorithm>

namespace cjson {
  namespace types {
    namespace __impl {
      class posinf { };
      class neginf { };
      class nan { };
      class null { };
    }
    // Bool, String
    using Bool = bool;
    using String = std::string;
    // Integers
    using Integer8 = std::int8_t;
    using Integer16 = std::int16_t;
    using Integer32 = std::int32_t;
    using Integer64 = std::int64_t;
    using UInteger8 = std::uint8_t;
    using UInteger16 = std::uint16_t;
    using UInteger32 = std::uint32_t;
    using UInteger64 = std::uint64_t;
    // Floating point
    using Float = float;
    using Double = double;
    // Special
    using Nan = __impl::nan;
    using Null = __impl::null;
    using NegInf = __impl::neginf;
    using PosInf = __impl::neginf;

    namespace __impl {
      using base_t = std::variant<
        Bool, String, Integer8, Integer16, Integer32, Integer64, UInteger8,
        UInteger16, UInteger32, UInteger64, Float, Double, NegInf, PosInf, Nan
      >;
      using sequance_t = std::variant<
        std::map<String, base_t>,
        std::vector<base_t>
      >;
      using value_t = std::variant<
        sequance_t, base_t
      >;
    }
    using Value = __impl::value_t;
  }

  namespace compiler {
    struct stream {
      std::vector<std::uint8_t> buffer;
      typedef std::basic_string<std::uint8_t> u8string;
      stream(): buffer() { }
      stream& feed(uint8_t byte) {
        buffer.push_back(byte);
        return *this;
      }
      u8string str() {
        u8string str;
        for ( std::uint8_t& byte : buffer )
          str.push_back(byte);
        return str;
      }
    };
    struct BaseValueCompiler {
      typedef stream& S;
      static void operator()(S s, types::Bool const& v) { s.feed(2 | v); }
      static void operator()(S s, types::String const& v) {
        if ( v.length() < 16 )
          s.feed(0xa0 | (v.length() & 0xf));
        else feed_number(s, v.size(), 0xb0);
        for ( uint8_t byte : v ) s.feed(byte);
      }
      static void feed_number(S s, uint64_t v, uint8_t mask) {
        uint64_t val = 0xff;
        uint8_t* b = (uint8_t*)&v, c = 1;
        for ( int idx = 0; idx <= 9; ++idx ) {
          if ( v <= val ) break;
          val = (val << 8) | 0xff;
          c++; b++;
        }
        s.feed(mask | c);
        for ( ; c > 0; c++, b++ )
          s.feed(*b);
      }
      static void operator()(S s, types::Integer8 const& v) {
        feed_number(s, v, 0x20);
      }
      static void operator()(S s, types::Integer16 const& v) {
        feed_number(s, v, 0x20);
      }
      static void operator()(S s, types::Integer32 const& v) {
        feed_number(s, v, 0x20);
      }
      static void operator()(S s, types::Integer64 const& v) {
        feed_number(s, v, 0x20);
      }
      static void operator()(S s, types::UInteger8 const& v) {
        feed_number(s, v, 0x30);
      }
      static void operator()(S s, types::UInteger16 const& v) {
        feed_number(s, v, 0x30);
      }
      static void operator()(S s, types::UInteger32 const& v) {
        feed_number(s, v, 0x30);
      }
      static void operator()(S s, types::UInteger64 const& v) {
        feed_number(s, v, 0x30);
      }
      static void operator()(S s, types::Float const& v) {
        feed_number(s, *(uint32_t*)&v, 0x40);
      }
      static void operator()(S s, types::Double const& v) {
        feed_number(s, *(uint64_t*)&v, 0x40);
      }
      static void operator()(S s, types::Nan const& v) { s.feed(1); }
      static void operator()(S s, types::Null const& v) { s.feed(0); }
      static void operator()(S s, types::PosInf const& v) { s.feed(4); }
      static void operator()(S s, types::NegInf const& v) { s.feed(5); }
    };
    struct Compiler {
    };
  }

  enum class base_value: uint8_t {
    Null, Nan, False, True, PosInf, NegInf
  };
  enum class object_policy: bool {
    pairwise, partition
  };
  enum class size_policy: bool {
    embedded, external
  };
  inline constexpr bool is_float(uint8_t byte) {
    return byte & 0x40;
  }
  inline constexpr bool is_integer(uint8_t byte) {
    return byte & 0x20;
  }
  inline constexpr bool sign(uint8_t byte) {
    return byte & 0x10;
  }
  inline constexpr bool is_sequance(uint8_t byte) {
    return byte & 0x80;
  }
  inline constexpr bool is_number(uint8_t byte) {
    return not is_sequance(byte);
  }
  inline constexpr bool is_object(uint8_t byte) {
    return byte & 0x40;
  }
  inline constexpr bool is_string(uint8_t byte) {
    return byte & 0x20;
  }
  inline constexpr bool is_array(uint8_t byte) {
    return not is_string(byte);
  }
  inline constexpr size_policy seq_size(uint8_t byte) {
    using enum size_policy;
    return byte & 0x10 ? embedded : external;
  }
  inline constexpr uint8_t get_size(uint8_t byte) {
    return byte & 0x0f;
  }

}

#define P(E) std::cout << #E " = " << #E << '\n'

#include <bit>


auto main(int argc, char** argv) -> int {
  std::copyable<int>;
}
