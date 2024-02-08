#ifndef __SNN_MEMBER_VAR_POINTER_
#define __SNN_MEMBER_VAR_POINTER_

#include <type_traits>

namespace snn {
  template<class _Member_type, class _Member_class>
  using member_t = _Member_type _Member_class:: *;

  template<class _Member_type, class _Member_class>
  struct _Member_accessor {
    using member_type = member_t<_Member_type, _Member_class>;
    using member_class = _Member_class;
    member_type _M_member;
    _Member_accessor()
      : _M_member{ nullptr } { }
    _Member_accessor(member_type const &addr)
      : _M_member{ addr } { }
    _Member_accessor(member_type &&addr)
      : _M_member{ std::move(addr) } {
      addr = nullptr;
    }
    _Member_accessor(_Member_accessor const &_ma)
      : _M_member{ _ma._M_member } { }
    _Member_accessor(_Member_accessor &&_ma)
      : _M_member{ std::move(_ma._M_member) } {
      _ma._M_member = nullptr;
    }
    void operator=(_Member_accessor &&_ma) {
      this->_M_member = _ma._M_member;
      _ma._M_member = nullptr;
    }
    member_type operator*() const { return _M_member; }
    void operator=(_Member_accessor const &_ma) { this->_M_member = _ma._M_member; }
    operator bool() const { return _M_member == nullptr; }
    decltype(auto) get(member_class const &obj) const { return obj.*this->_M_member; }
    decltype(auto) get(member_class &obj) const { return obj.*this->_M_member; }
    decltype(auto) operator()(member_class const &obj) const { return get(obj); }
    decltype(auto) operator()(member_class &obj) const { return get(obj); }

    template<class _To = _Member_type>
    std::remove_cvref_t<_To> to(member_class const &obj) const {
      return get(obj);
    }
  };

  template<class _Member_type, class _Member_class>
  _Member_accessor<_Member_type, _Member_class>
    member(member_t<_Member_type, _Member_class> const &ptr) { return ptr; }
}

#endif //__SNN_MEMBER_VAR_POINTER_