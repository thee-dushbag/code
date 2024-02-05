#ifndef __SNN_TYPE_LIST_HPP_
#define __SNN_TYPE_LIST_HPP_

#include <type_traits>

namespace snn {
  namespace list {
    template<typename ...types>
    struct typelist;

    template<typename list>
    struct pop_left;
    template<typename _type, typename ...types>
    struct pop_left<typelist<_type, types...>> {
      using type = typelist<types...>;
    };

    template<typename list>
    struct pop_right;
    template<typename last, typename ...types>
    struct pop_right<typelist<types..., last>> {
      using type = typelist<types...>;
    };

    template<typename list>
    struct first_type;
    template<typename first, typename ...types>
    struct first_type<typelist<first, types...>> {
      using type = first;
    };

    template<typename type, typename list>
    struct push_left;
    template<typename _type, typename ...types>
    struct push_left<_type, typelist<types...>> {
      using type = typelist<_type, types...>;
    };

    template<typename type, typename list>
    struct push_right;
    template<typename _type, typename ...types>
    struct push_right<_type, typelist<types...>> {
      using type = typelist<types..., _type>;
    };

    template<typename list>
    struct reverse;
    template<typename ...types>
    struct reverse<typelist<types...>> : push_right<typename first_type<typelist<types...>>::type,
      typename reverse<typename pop_left<typelist<types...>>::type>::type> { };

    template<>
    struct reverse<typelist<>> {
      using type = typelist<>;
    };

    template<typename type, typename list>
    struct is_one_of;
    template<typename type, typename ...types>
    struct is_one_of<type, typelist<types...>>
      : std::bool_constant<(std::is_same_v<type, types> || ...)> { };
  }

  namespace typelist {
    template <typename T, T val>
    struct integral_constant {
      using type = T;
      constexpr static T value = val;
    };

    template <bool b>
    using bool_constant = integral_constant<bool, b>;

    using true_type = bool_constant<true>;
    using false_type = bool_constant<false>;

    template <typename... Types>
    struct type_list { };

    namespace __detail {
      template<bool>
      struct _conditional {
        template<typename Type, typename>
        using type = Type;
      };

      template<>
      struct _conditional<false> {
        template<typename, typename Type>
        using type = Type;
      };
    }

    template<bool b, typename tType, typename fType>
    struct if_then_else {
      using type = typename __detail::_conditional<b>::type<tType, fType>;
    };

    template<bool b, typename TrueType, typename FalseType>
    using if_then_else_t = if_then_else<b, TrueType, FalseType>::type;

    template <typename Type, typename TypeList>
    struct is_one_of;

    template <typename Type, typename... Types>
    struct is_one_of<Type, type_list<Types...>>
      : bool_constant<(std::is_convertible_v<Type, Types> || ...) || (std::is_constructible_v<Types, Type> || ...)> { };

    template <typename Type, typename... Types>
    constexpr bool is_one_of_v = is_one_of<Type, Types...>::value;
  }
}

#endif //__SNN_TYPE_LIST_HPP_