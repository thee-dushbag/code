#include <iostream>
#include <os.hpp>

Os::Os() noexcept {
  std::cout << "Setting up Arch OS.\n";
}

void Os::notify() const noexcept {
  std::cout << "Arch loaded successfully.\n";
}

Os::~Os() noexcept {
  std::cout << "Saving state. Arch OFFLINE.\n";
}

