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

  template<typename return_t, typename ...args_t>
  struct Task {
    using function_t = std::function<return_t(args_t...)>;
    Task() = delete;
    Task(function_t const &function, args_t const &...args)
      : function{ function }, arguments{ std::forward<args_t>(args)... } { }
    void operator()() {
      if constexpr (not std::is_same_v<return_t, void>)
        promise.set_value(std::apply(function, arguments));
      else {
        std::apply(function, arguments);
        promise.set_value();
      }
    }
    decltype(auto) get() {
      if constexpr (not std::is_same_v<return_t, void>)
        return result.get();
      result.get();
    }
  private:
    function_t function;
    std::tuple<args_t...> arguments;
    std::future<return_t> result;
    std::promise<return_t> promise;
  };

  template<typename callable_t, typename ...args_t>
    requires std::is_invocable_v<callable_t, args_t...>
  Task<std::invoke_result_t<callable_t, args_t...>, args_t...>
    make_task(callable_t &&callable, args_t &&...args) {
    return { callable, args... };
  }

  struct Worker {
    using task_factory_t = std::function<task_t()>;
    Worker() = delete;
    Worker(task_factory_t const &factory)
      : task_factory{ factory },
      executor{ std::bind(std::mem_fn(&Worker::_worker), *this) },
      working{ true } { }
    void close() {
      if (not working) return;
      working = false;
      executor.request_stop();
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
    Pool(std::size_t size) : size{ size }, tasks{ }, waiters{ }, workers{ } {
      decltype(auto) factory = std::bind(std::mem_fn(&Pool::get_task), *this);
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
    void close() {
      for (auto &worker : workers)
        worker.close();
      while (tasks.size())
        tasks.pop_back();
      auto noop = [] { };
      while (waiters.size()) {
        waiters.front().set_value(noop);
        waiters.pop_front();
      }
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
