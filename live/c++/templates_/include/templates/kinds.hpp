#ifndef __CPP_TEMPLATES_KINDS_HPP
#define __CPP_TEMPLATES_KINDS_HPP

/*
Types of templates currently in
C++
*/

namespace tmp {
  // Variable templates
  template<bool b>
  struct not__: std::bool_constant<not b> { };

  template<bool b>
  concept not_v = not__<b>::value;

  template<bool>
  struct not_: std::false_type { };

  template<>
  struct not_<false>: std::true_type { };

  template<bool b>
  constexpr bool not_v2 = not_<b>::value;

  template<typename Type>
    requires not_v<std::is_same_v<std::decay_t<Type>, int>>
  Type variable;

  // Alias templates
  template<typename Type>
  using alias = Type;

  // Function Templates
  template<typename Type>
  decltype(auto) function(Type&& arg) { return arg; }

  // Class templates
  template <typename Type>
  struct Class {
    Type value;
    Class(): value{ } { }
    explicit Class(Type const& v)
      : value{ v } { }
    explicit Class(Type&& v)
      : value{ std::move(v) } { }
  };
}

#endif //__CPP_TEMPLATES_KINDS_HPP