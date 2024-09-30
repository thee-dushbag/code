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

void update(std::atomic_uint &aint, unsigned &nint, unsigned loops) {
  while (loops)
    (aint++, nint++, loops--);
}

int main() {
  std::atomic_uint aint{0};
  unsigned nint{0};

  std::vector<std::jthread> threads(THREADS);

  for (int i = 0; i < THREADS; i++)
    threads.emplace_back(update, std::ref(aint), std::ref(nint), LOOPS);

  std::cout << "Expect Int: " << (LOOPS * THREADS) << '\n'
            << "Atomic Int: " << aint << '\n'
            << "Normal Int: " << nint << '\n';
}
