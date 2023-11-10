#ifndef __HEADER_UNIQUE_MACRO
#define __HEADER_UNIQUE_MACRO

#include <concepts>

namespace snn {
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
      get(_Class const& obj) const {
      return obj.*member;
    }

    decltype(auto)
      operator()(_Class const& obj) const {
      return get(obj);
    }

    template<NonVoid _Return>
    _Return to(_Class const& obj) const
      requires std::convertible_to<_Type, _Return> {
      return get(obj);
    }
  };

  template <NonVoid _Type, NonVoid _Class>
  _Member_value<_Type, _Class>
    member(member_t<_Type, _Class> mem) {
    return mem;
  }
}

#endif //__HEADER_UNIQUE_MACRO