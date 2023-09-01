#ifndef __GENERATOR_HPP
#define __GENERATOR_HPP

#include <coroutine>
#include <functional>

template <typename T>
struct generator
{
    struct promise_type;
    using handle_type = std::coroutine_handle<promise_type>;

    generator(handle_type h) : coro{h} {}
    handle_type coro;
    ~generator()
    {
        if (coro)
            coro.destroy();
    }
    generator(generator const &) = delete;
    generator &operator=(const generator &) = delete;
    generator(generator &&g) : coro{g.coro} { g.coro = nullptr; }
    generator &operator=(generator &&g)
    {
        coro = g.coro;
        g.coro = nullptr;
        return *this;
    }
    T value()
    {
        return coro.promise().current_value;
    }

    bool next()
    {
        coro.resume();
        return not coro.done();
    }

    operator T() { return value(); }
    operator bool() { return next(); }

    struct promise_type
    {
        promise_type() = default;
        ~promise_type() = default;
        auto initial_suspend()
        {
            return std::suspend_always{};
        }
        auto final_suspend() noexcept
        {
            return std::suspend_always{};
        }
        auto get_return_object()
        {
            return generator{handle_type::from_promise(*this)};
        }
        auto return_value(T i)
        {
            current_value = i;
            return std::suspend_never{};
        }
        auto yield_value(int value)
        {
            current_value = value;
            return std::suspend_always{};
        }
        void unhandled_exception()
        {
            std::exit(1);
        }
        T current_value;
    };
};

#endif //__GENERATOR_HPP