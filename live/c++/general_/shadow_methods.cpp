#include <iostream>

struct Hell {
  virtual void hell() const noexcept { std::cout << "Hell::hell()\n"; }
};

struct Base : public Hell {
  virtual void hell() const noexcept override { std::cout << "Base::hell()\n"; }
  virtual void one() const noexcept = 0;
  virtual void two() const noexcept { std::cout << "Base::two()\n"; }
  void three() const noexcept { std::cout << "Base::three()\n"; }
};

struct Base2 : public Hell {
  virtual void hell() const noexcept override {
    std::cout << "Base2::hell()\n";
  }
  virtual void four() const noexcept = 0;
  virtual void five() const noexcept { std::cout << "Base2::five()\n"; }
  void six() const noexcept { std::cout << "Base2::six()\n"; }
};

struct Child : public Base, public Base2 {
  void one() const noexcept override { std::cout << "Child::one()\n"; }
  void two() const noexcept override { std::cout << "Child::two()\n"; }
  void three() const noexcept { std::cout << "Child::three()\n"; }
  void four() const noexcept override { std::cout << "Child::four()\n"; }
  void five() const noexcept override { std::cout << "Child::five()\n"; }
  void six() const noexcept { std::cout << "Child::six()\n"; }
  void hell() const noexcept override { std::cout << "Child::hell()\n"; }
};

int main() {
  Child child;
  Base &base = child;
  Base2 &base2 = child;
  child.one();
  child.two();
  child.three();
  base.one();
  base.two();
  base.three();
  std::cout << '\n';
  child.four();
  child.five();
  child.six();
  base2.four();
  base2.five();
  base2.six();
  std::cout << '\n';
  child.Base::two();
  child.Base::three();
  child.Base2::five();
  child.Base2::six();
  std::cout << '\n';
  child.hell();
  child.Base::hell();
  child.Base2::hell();
}
