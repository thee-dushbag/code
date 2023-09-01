#ifndef __SNN_HEADER_FILES_
#define __SNN_HEADER_FILES_

#include <numeric>
#include <array>
#include <iostream>
#include <snn_data.hpp>
#include <bitset>

using dint = snn::utils::data<int>;

namespace snn::std_tutor
{

    void bitset()
    {
        std::cout << std::boolalpha;
        std::bitset<8> bits("00110101"s);
        std::cout << "[bits]: " << bits.to_string() << '\n';
        std::cout << "[bits]: " << (bits <<= 2).to_string() << '\n';
        std::cout << "[bits]: " << (bits >>= 2).to_string() << '\n';
        std::cout << "[bits]: " << bits.flip().to_string() << '\n';
        std::cout << "[bits.any()]: " << bits.any() << '\n';
        std::cout << "[bits.count()]: " << bits.count() << '\n';
        // bits = bits.set();
        std::cout << "[bits.all()]: " << bits.all() << '\n';
        // bits = bits.reset();
        std::cout << "[bits.none()]: " << bits.none() << '\n';
        bits = bits.flip();
        std::cout << "[bits.ulong()]: " << bits.to_ulong() << '\n';
    }

    namespace algo
    {
        void algo()
        {
            std::cout << std::boolalpha;
            std::array seq{61, 3, 5};
            std::array num{4, 6, 8, 10, 12, 7, 4, 4, 6, 61, 3, 5, 7, 9, 11, 21, 3, 4, 5, 6, 61, 3, 5, 8, 9};
            bool all_are_even = std::all_of(num.begin(), num.end(), is_even);
            Pvar(all_are_even);
            bool some_are_even = std::any_of(num.begin(), num.end(), is_even);
            Pvar(some_are_even);
            bool none_are_even = std::none_of(num.begin(), num.end(), is_even);
            Pvar(none_are_even);
            std::for_each(num.begin(), num.end(), [](int i)
                          { std::cout << i << " * " << i << " = " << i * i << '\n'; });
            auto seven = std::find(num.begin(), num.end(), 7);
            Pvar(*seven);
            if (some_are_even)
            {
                auto first_even = std::find_if(num.begin(), num.end(), is_even);
                Pvar(*first_even);
            }
            if (!all_are_even)
            {
                auto first_odd = std::find_if_not(num.begin(), num.end(), is_even);
                Pvar(*first_odd);
            }
            auto fend = std::find_end(num.begin(), num.end(), seq.begin(), seq.end());
            if (fend != num.end())
                std::cout << "Sequence found in num: " << fend - num.begin() << '\n';
            else
                std::cout << "Sequence not found in num.\n";
            fend = std::find_first_of(num.begin(), num.end(), seq.begin(), seq.end());
            if (fend != num.end())
                std::cout << "Element in both seq and num found: " << *fend << '\n';
            else
                std::cout << "No element in num is in seq.\n";
            fend = std::adjacent_find(num.begin(), num.end());
            if (fend != num.end())
                std::cout << "Consecutive values of " << *fend << " found in num\n";
            else
                std::cout << "No consecutive values are equal in num\n";
            std::cout << "There are " << std::count(num.begin(), num.end(), 61) << " '61' values in num.\n";
            std::cout << "There are " << std::count_if(num.begin(), num.end(), is_even) << " even numbers in num\n";
            std::array a1{1, 2, 3, 4, 5, 6, 7, 8, 9}, a2{1, 7, 8, 9, 5, 6, 2, 3, 4};
            auto pair = std::mismatch(a1.begin(), a1.end(), a2.begin());
            while (pair.first != a1.end())
            {
                if (pair.first != a1.end())
                    std::cout << "Mismatch: " << *pair.first << " to " << *pair.second << '\n';
                else
                    std::cout << "Sequences match perfectly\n";
                pair.first++;
                pair.second++;
                pair = std::mismatch(pair.first, a1.end(), pair.second);
            }
            std::cout << "Is a2 a permutation of a1: " << std::is_permutation(a1.begin(), a1.end(), a2.begin()) << '\n';
            fend = std::search(num.begin(), num.end(), seq.begin(), seq.end());
            if (fend != num.end())
                std::cout << "Sequence found in num: " << fend - num.begin() << '\n';
            else
                std::cout << "Sequence not found in num.\n";
            fend = std::search_n(num.begin(), num.end(), 2, 4);
            if (fend != num.end())
                std::cout << "Sequence found in num: " << fend - num.begin() << '\n';
            else
                std::cout << "Sequence not found in num.\n";
            std::array<int, 3> vals;
            std::copy(seq.begin(), seq.end(), vals.begin());
            for (int i : vals)
                std::cout << i << ' ';
            std::cout << '\n';
            std::copy_n(num.begin(), 3, vals.begin());
            for (int i : vals)
                std::cout << i << ' ';
            std::cout << '\n';
            std::copy_if(num.begin(), num.end(), vals.begin(), [](int i)
                         { return i % 2 == 1; });
            for (int i : vals)
                std::cout << i << ' ';
            std::cout << '\n';
        }
    }

    template <typename T>
    void print_array(T const &t)
    {
        std::cout << "\tValue: " << t << '\n';
    }
    template <typename T, typename Fn>
    void print_iter(T cont, Fn printter)
    {
        std::cout << "printting Iterator:------------------------\n";
        for (auto u : cont)
            printter(u);
        std::cout << "Done:--------------------------------------\n";
    }
    void numeric()
    {
        std::initializer_list<dint> num{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        std::initializer_list<dint> numsqr{1, 4, 9, 16, 25, 36, 49, 64, 81, 100};
        dint res = std::accumulate(num.begin(), num.end(), dint{0});
        std::cout << res << '\n';
        std::array<dint, 10> resdiff;
        std::adjacent_difference(numsqr.begin(), numsqr.end(), resdiff.begin());
        print_iter(resdiff, print_array<dint>);
        res = std::inner_product(num.begin(), num.end(), num.begin(), dint{0});
        print_iter(resdiff, print_array<dint>);
        std::cout << res << '\n';
        res = std::accumulate(numsqr.begin(), numsqr.end(), dint{0});
        std::cout << res << '\n';
        std::partial_sum(num.begin(), num.end(), resdiff.begin());
        print_iter(num, print_array<dint>);
        print_iter(resdiff, print_array<dint>);
        std::iota(resdiff.begin(), resdiff.end(), 1);
        print_iter(resdiff, print_array<dint>);
    }
    namespace variant
    {
        using namespace std::string_literals;
        using dint = snn::utils::data<int>;
        using dstr = snn::utils::data<std::string>;
        using dcha = snn::utils::data<char>;
#define Pvar(var) std::cout << #var << " = " << var << '\n'

        struct FunctorOne
        {
            template <typename T>
            void operator()(T const &t)
            {
                std::cout << "[Functor Value]: " << t << '\n';
            }
        };
        namespace snn
        {
            template <typename T>
            void print(T const &t)
            {
                std::cout << "[Value]: " << t << '\n';
            }
        }
        struct AllTypes
        {
            void operator()(dint const &d) { std::cout << "[dint]:=> " << d << '\n'; }
            void operator()(dstr const &d) { std::cout << "[dstr]:=> " << d << '\n'; }
            void operator()(dcha const &d) { std::cout << "[dcha]:=> " << d << '\n'; }
            void operator()(int const &d) { snn::print<int>(d); }
        };

        auto variant() -> void
        {
            std::variant<dint, dcha, dstr, int> var;
            AllTypes printer;
            var = dint{56};
            Pvar(std::get<0>(var));
            var = "Simon Nganga"s;
            Pvar(std::get<2>(var));
            var = dcha{'A'};
            Pvar(std::get<1>(var));
            var = dstr{"Simon Nganga"s};
            Pvar(std::get<2>(var));
            std::visit(FunctorOne(), var);
            std::visit(printer, var);
            var = dint{67};
            std::visit(printer, var);
            var = dcha{'F'};
            std::visit(printer, var);
            var = 34;
            std::visit(printer, var);
        }
    }
}

#endif //__SNN_HEADER_FILES_