#ifndef __SNN_TUPLE_HPP_
#define __SNN_TUPLE_HPP_
#include <snn_type_list.hpp>

namespace snn::tuple {
    template<typename... _>
    class Tuple;

    template<>
    class Tuple<> {};

    template<typename Head, typename ...Types>
    class Tuple<Head, Types...> {
        Head head;
        Tuple<Types...> Others;

    public:
        Tuple(): head{}, Others{} {}
        Tuple(Head head, Types... others): head{head}, Others{others...} {}
        Head& get_head() noexcept { return this->head; }
        Tuple<Types...>& get_others() noexcept { return this->Others; }
        Head const& get_c_head() const noexcept { return this->head; }
        Tuple<Types...> const& get_c_others() const noexcept { return this->Others; }
    };


    // template<unsigned N, typename ...Types>
    // constexpr void print(std::ostream &out, Tuple<Types...> const& tup) {
    //     print(tup.get_c_others)
    // }

    template<unsigned N, typename ...Types>
    constexpr auto get(Tuple<Types...>& tup) {
        if constexpr (N == 0) return tup.get_head();
        return get<N-1>(tup.get_others());
    }
}

#endif //__SNN_TUPLE_HPP_