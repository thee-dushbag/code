#ifndef __SNN_TYPE_LIST_
#define __SNN_TYPE_LIST_

#include <snn_type_traits.hpp>

namespace snn::type_list {
    template<typename... Types>
    struct typelist {};

    template<typename, typename>
    struct pushback;

    template<typename Type, typename ...Types>
    struct pushback<Type, typelist<Types...>> {
        using list = typelist<Types..., Type>;
    };

    template<typename>
    struct popback;

    template<typename Type, typename ...Types>
    struct popback<typelist<Types..., Type>> {
        using list = typelist<Types...>;
        using type = Type;
    };

    template<typename, typename>
    struct pushfront;

    template<typename Type, typename ...Types>
    struct pushfront<Type, typelist<Types...>> {
        using list = typelist<Type, Types...>;
    };

    template<typename>
    struct popfront;

    template<typename Type, typename ...Types>
    struct popfront<typelist<Type, Types...>> {
        using list = typelist<Types...>;
        using type = Type;
    };

    template<typename, typename>
    struct is_one_of;

    template<typename Type, typename ...Types>
    struct is_one_of<Type, typelist<Types...>>
    :trait::bool_constant<trait::and__<trait::is_same_v<Type, Types> ...>> {};
}

#endif //__SNN_TYPE_LIST_
