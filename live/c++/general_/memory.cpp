#include <iostream>
#include <memory>

struct Value {
  Value() = delete;
  Value(int id) : id{ id } {
    std::cout << "Created: " << id << '\n';
  }
  ~Value() {
    std::cout << "Destroyed: " << id << '\n';
  }
private:
  int id;
};


struct Line {
  Line() { draw(); }
  ~Line() { draw(); }
  void draw() const {
    std::cout << "-----------------------------------------\n";
  }
};


auto main(int argc, char **argv) -> int {
  {
    Line _;
    std::unique_ptr<Value> v2;
    std::cout << "no_value: v2=" << v2.get() << '\n';
    std::unique_ptr<Value> v1{ new Value{ 2002 } };
    std::cout << "address: v1=" << v1.get() << '\n';
    auto v3 = std::make_unique<Value>(2010);
    std::cout << "address: v3=" << v3.get() << '\n';
    std::swap(v1, v3);
    std::cout << "new_addrs: v1=" << v1.get() << " v3=" << v3.get() << '\n';
    v1.reset(v3.release());
    std::cout << "reset/release: v1=" << v1.get() << " v3=" << v3.get() << '\n';
  }
  std::cout << '\n';
  {
    Line _;
    std::shared_ptr<Value> o;
    {
      Line _;
      std::shared_ptr<Value> i1;
      std::cout << "o: " << o.use_count() << '\n';
      {
        Line _;
        auto i = std::make_shared<Value>(3045);
        auto temp = std::make_shared<Value>(1111);
        std::cout << "temp: " << temp.use_count() << '\n';
        o = i;
        std::cout << "i: " << i.use_count() << '\n';
      }
    }
  }
}