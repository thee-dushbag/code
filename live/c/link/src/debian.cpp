#include <iostream>
#include <os.hpp>

Os::Os() noexcept {
  std::cout << "Setting up Debian OS.\n";
}

void Os::notify() const noexcept {
  std::cout << "Debian loaded successfully.\n";
}

Os::~Os() noexcept {
  std::cout << "Saving state. Debian OFFLINE.\n";
}

