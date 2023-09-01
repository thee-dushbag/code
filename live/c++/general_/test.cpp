module;
#include <iostream>
export module test;

export namespace test {
    template<class T, class U>
    concept Addable = requires(T t, U u) { t + u; };
    template<class T>
    class Int {
        T x;
    public:
        Int(T x): x{x} {}
        Int operator+(Int const &y) const noexcept { return {x + y.x}; }
        Int operator+(T const &y) const noexcept { return {x + y}; }
        void operator+=(Int const &y) noexcept { x += y.x; }
        operator T &() noexcept { return x; }
        friend std::ostream &operator<<(std::ostream &out, Int const &y) {
            out << "Int(" << y.x << ")";
            return out;
        }
    };
    template<class T, class U>
        requires Addable<T, U>
    std::common_type_t<T, U> add(T const &t, U const &u) {
        std::cout << t << " + " << u << " = " << t + u << '\n';
        return t + u;
    }
}
