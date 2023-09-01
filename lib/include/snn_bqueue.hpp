#ifndef __SNN_BLOCKING_QUEUE_HPP_
#define __SNN_BLOCKING_QUEUE_HPP_

#include <queue>
#include <mutex>
#include <future>

namespace snn {
    struct bqueue_error: std::exception {
        virtual const char *what() const noexcept {
            return "An Error Occured.";
        }
    };
    struct no_result_error : bqueue_error {
        virtual const char *what() const noexcept {
            return "There are no more values in the bqueue.";
        }
    };
    struct closing_bqueue : bqueue_error {
        virtual const char *what() const noexcept {
            return "Closing bqueue";
        }
    };
    namespace __detail {
        template<typename QType>
        QType pop_queue(std::queue<QType> &queue) {
            QType front = std::move(queue.front());
            queue.pop();
            return front;
        }
    }
    template<typename Type>
    requires (not std::is_void_v<Type>)
    struct bqueue {
        bqueue(): _value_cache{}, _waiters_cache{}, _mut{} {}
        bqueue(std::queue<Type> const &init)
        : _value_cache{init}, _waiters_cache{}, _mut{} {}
        bqueue(std::queue<Type> &&init)
        : _value_cache{std::move(init)}, _waiters_cache{}, _mut{} {}
        void push(Type const &value) {
            std::lock_guard<std::mutex> _(this->_mut);
            if (not this->_waiters_cache.empty()) {
                auto fut = __detail::pop_queue(this->_waiters_cache);
                fut.set_value(value);
            } else this->_value_cache.push(value);
        }
        bqueue(bqueue &&init): _value_cache{std::move(init._value_cache)},
        _waiters_cache{std::move(init._waiters_cache)}, _mut{} {}
        void operator=(bqueue &&init) {
            this->close();
            this->_value_cache = std::move(init._value_cache);
            this->_waiters_cache = std::move(init._waiters_cache);
        }
        void operator=(bqueue const &init) = delete;
        bqueue(bqueue const &) = delete;
        std::future<Type> pop() {
            std::lock_guard<std::mutex> _(this->_mut);
            std::promise<Type> prom{};
            if (this->_value_cache.empty()) {
                auto fut = prom.get_future();
                this->_waiters_cache.push(std::move(prom));
                return fut;
            } else {
                auto value = __detail::pop_queue(this->_value_cache);
                prom.set_value(std::move(value));
                return prom.get_future();
            }
        }
        ~bqueue() noexcept { this->_notify_waiters<no_result_error>(); }

        std::queue<Type> close() {
            std::lock_guard<std::mutex> _(this->_mut);
            this->_notify_waiters<closing_bqueue>();
            return std::move(this->_value_cache);
        }
        bool empty() const { return this->_value_cache.empty(); }
        bool waiting() const { return this->_waiters_cache.empty(); }
        std::size_t size() const { return this->_value_cache.size(); }
        std::size_t waiters() const { return this->_waiters_cache.size(); }

    private:
        template<typename error_type>
        void _notify_waiters() noexcept {
            auto err_ptr = std::make_exception_ptr(error_type());
            std::promise<Type> waiter;
            while (not this->_waiters_cache.empty()) {
                waiter = __detail::pop_queue(this->_waiters_cache);
                waiter.set_exception(err_ptr);
            }
        }
        std::queue<Type> _value_cache;
        std::queue<std::promise<Type>> _waiters_cache;
        std::mutex _mut;
    };
}

#endif //__SNN_BLOCKING_QUEUE_HPP_