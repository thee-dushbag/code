#ifndef __SNN_TYPE_TRAITS_
#define __SNN_TYPE_TRAITS_

#include <snn_type_traits.hpp>

namespace snn::trait {
    template<typename Type, Type val>
    struct integral_constant {
        using type = Type;
        constexpr static Type value = val;
    };

    template<typename T>
    struct type_constant {
        using type = T;
    };

    template<bool ...b> constexpr bool xor__ = (b xor ...);
    template<bool ...b> constexpr bool and__ = (b and ...);
    template<bool ...b> constexpr bool or__= (b or ...);
    template<bool b> constexpr bool not__ = not b;

    template<bool b>
    struct bool_constant: integral_constant<bool, b> {};

    using true_type = bool_constant<true>;
    using false_type = bool_constant<false>;

    template<typename, typename>
    struct is_same: false_type {};

    template<typename T>
    struct is_same<T, T>: true_type {};

    template<typename Type, typename ...Types>
    struct are_same: bool_constant<and__<is_same<Type, Types>::value ...>> {};

    template<typename T>
    struct is_const: false_type {};

    template<typename T>
    struct is_const<T const>: true_type {};

    template<typename T>
    struct is_volatile: false_type {};

    template<typename T>
    struct is_const<T volatile>: true_type {};

    template<typename T>
    struct add_const: type_constant<T const> {};

    template<typename T, typename U>
    constexpr bool is_same_v = is_same<T, U>::value;

    template<typename T>
    constexpr bool is_const_v = is_const<T>::value;

    template<typename T>
    using add_const_t = typename add_const<T>::type;

    template<typename T>
    struct rm_const: type_constant<T> {};

    template<typename T>
    struct rm_const<T const>: type_constant<T> {};

    template<typename T>
    using rm_const_t = typename rm_const<T>::type;
}

#endif //__SNN_TYPE_TRAITS_