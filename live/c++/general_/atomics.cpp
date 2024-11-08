#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

#ifndef THREADS
# define THREADS 10
#endif

#ifndef LOOPS
# define LOOPS 200
#endif

std::atomic_uint aint{0};
unsigned nint{0};

void update(std::atomic_uint &aint, unsigned &nint, unsigned loops) {
  while (loops)
    (aint++, nint++, loops--);
}

int main(int, char**) {
  {
    std::vector<std::thread> threads(THREADS);
    for (int i = 0; i < THREADS; i++)
      threads.emplace_back(update, std::ref(aint), std::ref(nint), LOOPS);
    /*for (auto &thread: threads)*/
    /*  if (thread.joinable())*/
    /*    thread.join();*/
  }

  std::cout << "Expect Int: " << (LOOPS * THREADS) << '\n'
            << "Atomic Int: " << aint << '\n'
            << "Normal Int: " << nint << '\n';
}
