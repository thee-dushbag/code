#define LOG_SNN_DATA
#include <iostream>
#include <snn_data.hpp>
#include <snn_utils.hpp>
#include <string>
#include <vector>

using namespace snn::utils;

template<typename Type>
struct type_constant
{ typedef Type type; };

template<uint Size>
struct pack_size
{ static constexpr uint size = Size; };

template<std::size_t N, typename... Types>
struct nth_type;

template<typename T0, typename ...Types>
struct nth_type<0, T0, Types...>
: type_constant<T0> {};

template<typename T0, typename T1, typename ...Types>
struct nth_type<1, T0, T1, Types...>
: type_constant<T1> {};

template<typename T0, typename T1, typename T2, typename ...Types>
struct nth_type<2, T0, T1, T2, Types...>
: type_constant<T2> {};

template<typename T0, typename T1, typename T2, typename T3, typename ...Types>
struct nth_type<3, T0, T1, T2 , T3, Types...>
: type_constant<T3> {};

template<std::size_t N, typename T0, typename T1, typename T2, typename ...Types>
struct nth_type<N, T0, T1, T2, Types...>
: nth_type<N - 3, Types...> {};

auto main(int argc, char **argv) -> int {
    nth_type<4, int, double, std::string, char, long>::type;
}