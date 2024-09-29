#include <iostream>
#include <os.hpp>

Os::Os() noexcept {
  std::cout << "Setting up Manjaro OS.\n";
}

void Os::notify() const noexcept {
  std::cout << "Manjaro loaded successfully.\n";
}

Os::~Os() noexcept {
  std::cout << "Saving state. Manjaro OFFLINE.\n";
}

