#ifndef __SNN_EVENTS_HPP_IMPL__
#define __SNN_EVENTS_HPP_IMPL__

#include <unordered_map>
#include <concepts>
#include <string>
#include <vector>
#include <future>
#include <mutex>

namespace snn::events {
    using event_type = std::string;

    struct event_functor
    { virtual void operator()(const event_type&) = 0; };

    class event_emitter {
        std::unordered_map<event_type, std::vector<event_functor *>> _events;
        std::mutex _lock;
    public:
        event_emitter(): _events{}, _lock{} {}
        event_emitter(event_emitter &&other)
        : _events{std::move(other._events)}, _lock{} {}
        event_emitter(event_emitter const &) = delete;
        void operator=(event_emitter const &) = delete;
        void operator=(event_emitter &&e)
        { this->_events = std::move(e._events); }
        void emit(const event_type&);
        void drop(const event_type&);
        void listen(const event_type&, event_functor *);
        void forget(const event_type&, event_functor *);
        template<typename ...event_functors>
        requires (std::derived_from<event_functors, event_functor> && ...)
        void listeners(event_type const&, event_functors *...);
        std::vector<event_functor *> &operator[](event_type const &);
        bool contains(event_type const &) const;
    };

    template<typename _Functor, typename... _Args>
        requires std::invocable<_Functor, event_type, _Args...>
    class event_handle: public event_functor {
        using _result_type = std::invoke_result_t<_Functor, event_type, _Args...>;
        constexpr static bool _result_is_safe = (!std::same_as<_result_type, void>);
        using _safe_result_type = std::conditional_t<_result_is_safe, _result_type, bool>;

        _Functor function;
        std::tuple<_Args...> args;
        _safe_result_type result;

        void _invoke (std::tuple<event_type, _Args...> &true_args)
        requires _result_is_safe
        { this->result = std::apply(this->function, true_args); }

        void _invoke (std::tuple<event_type, _Args...> &true_args)
        requires (!_result_is_safe)
        { std::apply(this->function, true_args); }

        void invoke(const event_type&event)
        { std::tuple<event_type, _Args...> true_args =
          std::tuple_cat(std::tuple<event_type>{event}, this->args);
          this->_invoke(true_args); }

    public:
        event_handle() = delete;

        event_handle(_Functor &&func, _Args &&... args)
        : function{std::forward<_Functor>(func)},
            args{std::forward<_Args>(args)...},
            result{} {}

        decltype(auto) get_result()
        { return this->result; }

        constexpr bool has_result() const
        { return _result_is_safe; };

        void operator()(const event_type &event)
        { this->invoke(event); }
    };

    void event_emitter::emit(const event_type& event) {
        std::lock_guard<std::mutex> _{this->_lock};
        if (not this->_events.contains(event)) return;
        std::vector<event_functor *> &targets = this->_events[event];
        std::vector<std::future<void>> futs{targets.size()};
        for (auto &target: targets)
            futs.push_back(std::async(std::launch::async,
            [&](){ (*target)(event); }));
    }

    void event_emitter::drop(const event_type& event) {
        std::lock_guard<std::mutex> _{this->_lock};
        this->_events.erase(event);
    }

    void event_emitter::listen(const event_type& event, event_functor *functor) {
        std::lock_guard<std::mutex> _{this->_lock};
        this->_events[event].push_back(functor);
    }

    template<typename... event_functors>
        requires (std::derived_from<event_functors, event_functor> && ...)
    void event_emitter::listeners(const event_type &event, event_functors *...functors)
    { ([&](){this->listen(event, functors); return true; }() && ...); }

    void event_emitter::forget(const event_type& event, event_functor *functor) {
        if (not this->_events.contains(event)) return;
        std::vector<event_functor *> &targets = this->_events[event];
        std::vector<event_functor *>::iterator found;
        bool found_flag{false};
        for (auto iter = targets.begin(); iter != targets.end(); iter ++)
            if (*iter == functor) { found_flag = true; found = iter; break; }
        if (found_flag)
        { std::lock_guard<std::mutex> _{this->_lock}; targets.erase(found); }
    }

    std::vector<event_functor *> &event_emitter::operator[](event_type const &event)
    { return this->_events[event]; }

    bool event_emitter::contains(event_type const &event) const
    { return this->_events.contains(event); }

    template<typename Functor>
    struct consume_event {
        Functor function;
        consume_event() = delete;
        consume_event(Functor func)
        : function{func} {}

        template<typename _EventType, typename... Args>
        requires (!std::same_as<std::invoke_result_t<Functor, Args...>, void>)
        std::invoke_result_t<Functor, Args...>
        operator()(_EventType const &, Args &&...args)
        { return this->function(std::forward<Args>(args)...); }

        template<typename _EventType, typename... Args>
        requires std::same_as<std::invoke_result_t<Functor, Args...>, void>
        void operator()(_EventType const &, Args &&...args)
        { this->function(std::forward<Args>(args)...); }
    };

    template<typename Functor, typename... Args>
    event_handle<Functor, Args...>
    make_handle(Functor &&func, Args &&...args)
    { return {std::forward<Functor>(func),
      std::forward<Args>(args)...}; }

    template<typename Functor, typename... Args>
    event_handle<consume_event<Functor>, Args...>
    make_chandle(Functor &&func, Args &&...args)
    { return {{std::forward<Functor>(func)},
      std::forward<Args>(args)...}; }
}

#endif //__SNN_EVENTS_HPP_IMPL__