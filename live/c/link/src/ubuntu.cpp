#include <iostream>
#include <os.hpp>

Os::Os() noexcept {
  std::cout << "Setting up Ubuntu OS.\n";
}

void Os::notify() const noexcept {
  std::cout << "Ubuntu loaded successfully.\n";
}

Os::~Os() noexcept {
  std::cout << "Saving state. Ubuntu OFFLINE.\n";
}

