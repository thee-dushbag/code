#ifndef _SNN_POOL_HPP_
#define _SNN_POOL_HPP_

#include <forward_list>
#include <functional>
#include <future>
#include <iostream>
#include <queue>
#include <thread>

namespace snn {
  using task_type = std::function<void()>;

  struct Worker {
    Worker() = delete;
    Worker(std::function<task_type()> get_task)
        : working{true}, get_task{get_task},
          thread{std::mem_fn(&Worker::work), std::ref(*this)} {
      std::cout << "Worker Up\n";
    }
    Worker(const Worker &) = delete;
    ~Worker() { std::cout << "Worker Down\n"; }
    void work() {
      while (working)
        get_task()();
    }
    void shutdown() { working = false; }
    bool working;
    std::function<task_type()> get_task;
    std::jthread thread;
  };

  struct Pool {
    Pool() = delete;
    Pool(size_t size) : tasks{}, workers{}, waiters{} {
      auto get_task = std::bind(std::mem_fn(&Pool::get_task), std::ref(*this));
      for (; size; --size)
        workers.emplace_front(get_task);
    }
    task_type get_task() {
      if (tasks.size()) {
        auto &&task = std::move(tasks.front());
        tasks.pop();
        return task;
      }
      std::promise<task_type> prom;
      auto future = prom.get_future();
      waiters.push(std::move(prom));
      return future.get();
    }
    void put_task(task_type task) {
      if (waiters.size()) {
        auto &&waiter = std::move(waiters.front());
        waiters.pop();
        waiter.set_value(task);
      } else
        tasks.push(task);
    }
    void shutdown() {
      for (auto &worker : workers)
        worker.shutdown();
      auto noop = [] {};
      while (tasks.size())
        tasks.pop();
      while (waiters.size()) {
        waiters.front().set_value(noop);
        waiters.pop();
      }
    }

    void wait() {
      std::mutex lock;
      lock.lock();
      put_task([&lock] { lock.unlock(); });
      std::lock_guard _{lock};
      // while (tasks.size())
      // std::this_thread::yield();
    }
    std::queue<task_type> tasks;
    std::forward_list<Worker> workers;
    std::queue<std::promise<task_type>> waiters;
  };
} // namespace snn

#endif //_SNN_POOL_HPP_
