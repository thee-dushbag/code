#ifndef __SNN_EVENTS_HPP_
#define __SNN_EVENTS_HPP_

#include <string>
#include <list>
#include <future>
#include <unordered_map>

namespace snn::events
{
    struct functor
    {
        virtual void operator()() = 0;
    };

    class event
    {
        std::unordered_map<std::string, std::list<functor *>> event_rg;

    public:
        event() : event_rg{} {}
        event(std::unordered_map<std::string, std::list<functor *>> const &events)
            : event_rg{events} {}
        event(std::unordered_map<std::string, std::list<functor *>> &&events)
            : event_rg{std::move(events)} {}

        void emit(std::string const &event)
        {
            if (not this->event_rg.contains(event))
                return;
            auto &targets = this->event_rg[event];
            std::list<std::future<void>> futs;
            for (auto &func : targets)
                futs.push_back(std::async(std::launch::async, [&](){ (*func)(); }));
            for (auto &fut : futs)
                fut.get();
        }

        void subscribe(std::string const &event, functor *func)
        {
            if (not this->event_rg.contains(event))
                this->event_rg[event] = {};
            this->event_rg[event].push_back(func);
        }

        template <typename... Type>
        void subscribe_all(std::string const &event, Type *...func)
        {
            std::initializer_list<void *> vals{func...};
            for (auto &val : vals)
                subscribe(event, (functor *)val);
        }

        void drop_event(std::string const &event)
        {
            if (this->event_rg.contains(event))
                this->event_rg.erase(event);
        }
    };
    template <bool cond, typename true_type, typename false_type>
    struct _if_then_else;

    template <typename true_type, typename false_type>
    struct _if_then_else<true, true_type, false_type>
    {
        using type = true_type;
    };

    template <typename true_type, typename false_type>
    struct _if_then_else<false, true_type, false_type>
    {
        using type = false_type;
    };

    template <typename Type>
    concept _is_void = std::is_same_v<Type, void>;
    
    template <typename Function, typename... Args>
        requires std::invocable<Function, Args...>
    class event_handler : public snn::events::functor
    {
        Function function;
        std::tuple<Args...> args;
        using _ResultType = std::invoke_result_t<Function, Args...>;
        using ResultType = _if_then_else<std::is_same_v<_ResultType, void>, bool, _ResultType>::type;
        ResultType result{};
        void _invoke()
        {
            if constexpr (_is_void<_ResultType>)
                std::apply(function, args);
            else
                result = std::apply(function, args);
        }

    public:
        event_handler(Function func, Args... args) : function{func}, args{args...} {}
        void operator()() override
        {
            _invoke();
        }
        constexpr bool has_result() const noexcept
        {
            return (!_is_void<_ResultType>);
        }
        ResultType get_result() const noexcept
        {
            return result;
        }
    };
}

#endif //__SNN_EVENTS_HPP_
