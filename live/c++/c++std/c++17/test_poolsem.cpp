#include <iostream>
#include <functional>
#include <thread>
#include <queue>
#include "sem.hpp"
#include "utils.hpp"
#include <cstdlib>
#include "pool.hpp"
#include <chrono>

using snn::_17::Semaphore;
using snn::_17::Session;

void task(std::string const &name, int const &delay, Semaphore &sem) {
  snn::print("[Task: ", name, "]: Acquire.");
  Session _{ sem };
  snn::print("[Task: ", name, "]: Starting.");
  std::this_thread::sleep_for(std::chrono::milliseconds(delay));
  snn::print("[Task: ", name, "]: Done.");
}

void pool_task(std::string const &name, int delay) {
  snn::print("[Task: ", name, "]: Starting.");
  std::this_thread::sleep_for(std::chrono::milliseconds(delay));
  snn::print("[Task: ", name, "]: Done.");
}

std::string task_name(size_t const &id) {
  return std::to_string(id);
}

int time_sec(int const &start, int const &stop) {
  return start + (std::rand() % (stop - start));
}

void tasks_via_semaphore(int size, std::vector<int> const &delays) {
  Semaphore sem{ size };
  std::vector<std::jthread> tasks;
  for (size_t idx = 1; idx <= delays.size(); ++idx)
    tasks.emplace_back(task, task_name(idx), delays[idx], std::ref(sem));
}

void tasks_via_pool(int size, std::vector<int> const &delays) {
  snn::Pool pool{ size_t(size) };
  for (size_t idx = 1; idx <= delays.size(); ++idx)
    pool.put_task(std::bind(pool_task, task_name(idx), delays[idx]));
  pool.wait();
  pool.shutdown();
}

std::vector<int> get_delays(int size, int start, int stop) {
  std::srand(std::time(NULL));
  std::vector<int> delays;
  for (; size > 0; --size)
    delays.push_back(time_sec(start, stop));
  return delays;
}

auto main(int argc, char **argv) -> int {
  auto delays = get_delays(300, 250, 5001);
  tasks_via_semaphore(10, delays); // Very Expensive. Type issues with the semaphore.
  tasks_via_pool(10, delays); // Lighter, very buggy. Some crashes are expected.
}
