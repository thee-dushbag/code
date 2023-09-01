#define LOG_SNN_DATA
#include <snn_utils.hpp>
#include "review.hpp"
#include <iostream>
#include <string>
#include <memory>
#include <snn_alloc.hpp>
#include <tuple>
#include <climits>
#include <snn_data.hpp>

using snn::utils::print;
using snn::utils::data;

template<typename... First>
struct zip {
    template<typename... Second>
    requires (sizeof...(First) == sizeof...(Second))
    struct with {
        std::tuple<std::pair<First, Second> ...> zipped;
        with(const First &...first, const Second& ...second)
        : zipped{{first, second} ...} {}
    };
};

template<typename T>
void print_me(const std::shared_ptr<T> &s)
{ std::cout << *s << '\n'; }


auto main(int argc, char** argv) -> int {
    auto prt = std::make_unique<data<std::string>>("Simon Nganga. Faith Njeri. Lydia Wanjiru");
    print(*prt);
    print(ULONG_LONG_MAX + 2);
}