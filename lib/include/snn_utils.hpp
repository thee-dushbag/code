#ifndef __SNN_UTILS_HPP_
#define __SNN_UTILS_HPP_

#include <mutex>
#include <iostream>
#include <string>
#include <fstream>
#include <filesystem>
#include <concepts>

namespace snn::utils {
    std::mutex gmut;

    namespace __detail {
        template <typename O, typename... T>
        void print_impl(O &out, T const &...t) {
            std::lock_guard<std::mutex> _lock(gmut);
            (out << ... << t);
        }
        template <typename O, typename... T>
        void print_impl_ln(O &out, T const &...t) {
            std::lock_guard<std::mutex> _lock(gmut);
            (out << ... << t) << '\n';
        }
    }

    template <typename... T>
    void printo(std::ostream &out, T &&...t) {
        __detail::print_impl(out, std::forward<T>(t) ...);
    }

    template <typename... T>
    void print(T &&...t) {
        __detail::print_impl(std::cout, std::forward<T>(t) ...);
    }

    template <typename... T>
    void println(T &&...t) {
        __detail::print_impl_ln(std::cout, std::forward<T>(t) ...);
    }

    class filesystem_error : public std::exception {
        std::string reason;
    public:
        filesystem_error(std::string const& reason)
            : reason{ reason } {}
        const char* what() const noexcept override
        {
            return this->reason.c_str();
        }
    };

    std::string read_file(std::string const& filename) {
        std::filesystem::path path{ filename };
        if (not std::filesystem::exists(path))
            throw filesystem_error(std::string("Path does not exist: ") + std::string(path));
        if (not std::filesystem::is_regular_file(path))
            throw filesystem_error(std::string("Not a file: ") + std::string(path));
        std::ifstream file{ filename.c_str(), std::ios::in };
        auto file_size = std::filesystem::file_size(path);
        std::string contents;
        contents.resize(file_size + 1);
        file.readsome(contents.data(), file_size);
        file.close();
        return contents;
    }
    template<typename T>
    T add(T const& x, T const& y) {
        print(x, " + ", y, " = ", x + y);
        return x + y;
    }

    template<typename T>
    T mul(T const& x, T const& y) {
        print(x, " * ", y, " = ", x * y);
        return x * y;
    }

    template<typename T>
    T sub(T const& x, T const& y) {
        print(x, " - ", y, " = ", x - y);
        return x - y;
    }
}

#endif //__SNN_UTILS_HPP_