#ifndef _SNN_SEM_HPP_17
#define _SNN_SEM_HPP_17

#include <thread>
#include <queue>

namespace snn::_17 {
  namespace __detail {
    struct Wait {
      Wait() : locked{ true } { }
      void wait() {
        while (locked)
          std::this_thread::yield();
      }
      void unlock() {
        locked = false;
      }
    private:
      bool locked;
    };
  }

  struct Semaphore {
    Semaphore() = delete;
    Semaphore(int max) : max{ max }, waiters{ } {
      if (max < 1)
        throw "max cannot be negative or zero.";
    }
    ~Semaphore() {
      if (waiters.size() > 0)
        throw "There are waiters waiting for a session.";
    }
    friend struct Session;
  private:
    void release() {
      if (waiters.size() > 0) {
        __detail::Wait &waiter = *waiters.front();
        waiters.pop();
        waiter.unlock();
      }
      else max++;
    }

    void acquire() {
      if (max == 0) {
        __detail::Wait waiter;
        waiters.push(&waiter);
        waiter.wait();
      }
      else max--;
    }
    int max;
    std::queue<__detail::Wait *> waiters;
  };

  struct Session {
    Session() = delete;
    Session(Semaphore &sem)
      : sem{ sem } {
      sem.acquire();
    }
    ~Session() { sem.release(); }
  private:
    Semaphore &sem;
  };
}

#endif //_SNN_SEM_HPP_17