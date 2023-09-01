#ifndef __CLASS_TEMPLATES_SNN_HPP_
#define __CLASS_TEMPLATES_SNN_HPP_

#include <iostream>
#include <typeinfo>
#include <func_tmps.hpp>
#include <snn_type_list.hpp>

using snn::utils::print;
using snn::typelist::is_one_of_v;
using StringTypes = snn::typelist::type_list<std::string, const char*, char>;
template<typename T>
concept StringLike = is_one_of_v<T, StringTypes>;

namespace tmps::cls {
    template<typename T>
    struct Storage {
        Storage(): store {} {}
        Storage(T const &t): store{t} {}
        Storage(T&& t): store{std::move(t)} {}
        friend std::ostream &operator<<(std::ostream &out, Storage const &s) {
            out << "Storage(value='" << s.store << "', type='" << s.type_name << "')";
            return out;
        }
        void say_hi();
    private:
        T store;
        const char *type_name{typeid(T).name()};
    };

    template<typename T>
    void Storage<T>::say_hi() {
        print("Hello There: I am storing ", store);
    }
    template<>
    void Storage<std::string>::say_hi() {
        print("Hello: I am storing a string and I will not tell you what?");
    }
}

#endif //__CLASS_TEMPLATES_SNN_HPP_