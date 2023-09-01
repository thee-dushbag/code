#ifndef __FUNCTION_TEMPLATES_HPP_
#define __FUNCTION_TEMPLATES_HPP_

#include <type_traits>
#include <snn_utils.hpp>
#include <snn_type_list.hpp>

namespace tmps::func {
    using snn::utils::print;
    using StringTypes = snn::typelist::type_list<std::string, char *, const char *>;
    template<typename Type>
    concept StringLike = snn::typelist::is_one_of_v<std::decay_t<Type>, StringTypes>;
    template<typename T, typename U>
    std::common_type_t<T, U> max(T const &a, U const &b) {
        return b > a? b : a;
    }
    template<typename T>
        requires StringLike<T>
    void say_hi(T const& name) {
        print("Hello ", name, ", how was your day?");
    }
    void say_hi(...) {
        print("Passed Name is Not Valid");
    }
}

#endif //__FUNCTION_TEMPLATES_HPP_