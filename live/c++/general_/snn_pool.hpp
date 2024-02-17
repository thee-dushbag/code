#ifndef _SNN_POOL_HPP_
#define _SNN_POOL_HPP_

#include <thread>
#include <future>
#include <functional>
#include <tuple>
#include <deque>
#include <forward_list>

namespace snn {
  using task_t = std::function<void()>;

  template<typename callable_t, typename ...args_t>
  class Task {
    callable_t function;
    std::tuple<args_t...> arguments;
    using return_t = std::invoke_result_t<callable_t, args_t...>;
    std::conditional_t<std::is_void_v<return_t>, bool, return_t> result;
    bool event;
  public:
    Task() = delete;
    Task(callable_t const &function, args_t const &...args)
      : function{ function }, arguments{ args... }, event{ false } { }
    return_t get() {
      while (not event)
        std::this_thread::yield();
      if constexpr (not std::is_void_v<return_t>)
        return result;
    }
    void operator()() {
      if (event) return;
      if constexpr (std::is_void_v<return_t>)
        std::apply(function, arguments);
      else result = std::apply(function, arguments);
      event = true;
    }
  };

  struct Worker {
    using task_factory_t = std::function<task_t()>;
    Worker() = delete;
    Worker(task_factory_t const &factory)
      : task_factory{ factory },
      executor{ std::bind(std::mem_fn(&Worker::_worker), std::ref(*this)) },
      working{ true } { }
    void close() {
      if (not working) return;
      working = false;
    }
  private:
    void _worker() {
      while (working)
        task_factory()(); // Get a task and execute it!
    }
    task_factory_t task_factory;
    std::jthread executor;
    bool working;
  };

  struct Pool {
    Pool() = delete;
    explicit Pool(std::size_t size) : size{ size }, tasks{ }, waiters{ }, workers{ } {
      decltype(auto) factory = std::bind(std::mem_fn(&Pool::get_task), std::ref(*this));
      for (std::size_t s = 0; s < size; ++s)
        workers.emplace_front(factory);
    }
    void put_task(task_t const &task) {
      if (waiters.size()) {
        waiters.front().set_value(task);
        waiters.pop_front();
      }
      else
        tasks.push_back(task);
    }
    void clear() {
      while (tasks.size())
        tasks.pop_back();
    }
    void close() {
      wait();
      for (auto &worker : workers)
        worker.close();
      auto noop = [] { };
      while (waiters.size()) {
        waiters.front().set_value(noop);
        waiters.pop_front();
      }
    }
    void wait() {
      while (tasks.size())
        std::this_thread::yield();
    }
    void breakpoint() {
      std::promise<void> waiter;
      auto future = waiter.get_future();
      put_task([&waiter] { waiter.set_value(); });
      future.get();
    }
    ~Pool() { close(); }
  private:
    task_t get_task() {
      std::promise<task_t> waiter;
      std::future<task_t> future = waiter.get_future();
      if (tasks.size()) {
        waiter.set_value(std::move(tasks.front()));
        tasks.pop_front();
      }
      else
        waiters.push_back(std::move(waiter));
      return future.get();
    }
    std::size_t size;
    std::deque<task_t> tasks;
    std::forward_list<Worker> workers;
    std::deque<std::promise<task_t>> waiters;
    friend struct Worker;
  };
}

#endif //_SNN_POOL_HPP_
