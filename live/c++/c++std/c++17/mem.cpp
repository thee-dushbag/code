#include <atomic>
#include <cassert>
#include <iostream>

template <class T>
struct __control_block {
  T *managed_pointer;
  std::atomic_uint32_t strong, weak;
};

template <class T>
struct default_deleter {
  void operator()(T *memory) const { delete memory; }
};

template <class T, class D>
class weak_ptr;

template <class T, class D = default_deleter<T>>
class shared_ptr {
  __control_block<T> *block;
  D deleter;

  shared_ptr(__control_block<T> *block): block(block) {
    if(block)
      block->strong++;
  }

public:
  friend class weak_ptr<T, D>;
  shared_ptr(): block(nullptr) { }
  shared_ptr(shared_ptr const &sp): block(sp.block) {
    if(block)
      block->strong++;
  }
  shared_ptr(T *payload): block(new __control_block<T>{payload, 1, 0}) { }
  shared_ptr &operator=(shared_ptr const &sp) {
    reset();
    if((block = sp.block))
      block->strong++;
    return *this;
  }
  D &get_deleter() const { return deleter; }
  std::uint32_t use_count() const {
    return block ? (unsigned)block->strong : 0;
  }
  T *get() const { return block ? block->managed_pointer : nullptr; }
  ~shared_ptr() { reset(); }
  T *operator->() const { return block->managed_pointer; }
  T &operator*() const { return *block->managed_pointer; }
  bool unique() const { return use_count() == 1; }
  operator bool() const { return use_count(); }
  void reset() {
    if(block) {
      block->strong--;
      if(block->strong == 0) {
        deleter(block->managed_pointer);
        block->managed_pointer = nullptr;
      }
      if(block->strong == 0 and block->weak == 0)
        delete block;
    }
    block = nullptr;
  }
};

template <class T, class D = default_deleter<T>>
class weak_ptr {
  __control_block<T> *block;
  D deleter;

public:
  weak_ptr(): block(nullptr), deleter() { }
  weak_ptr(shared_ptr<T, D> const &sp): block(sp.block), deleter(sp.deleter) {
    if(block)
      block->weak++;
  }
  weak_ptr(weak_ptr<T> const &wp): block(wp.block), deleter(wp.deleter) {
    if(block)
      block->weak++;
  }
  weak_ptr &operator=(weak_ptr const &wp) {
    reset();
    if((block = wp.block))
      wp.block->weak++;
    return *this;
  }
  operator bool() const { return use_count(); }
  shared_ptr<T, D> lock() const {
    return block ? (block->strong ? block : nullptr) : nullptr;
  }
  bool expired() const { return block ? block->strong == 0 : false; }
  std::uint32_t use_count() const {
    return block ? (unsigned)block->strong : 0;
  }
  T *get() const { return block ? block->managed_pointer : nullptr; }
  ~weak_ptr() { reset(); }
  void reset() {
    if(block) {
      block->weak--;
      if(block->strong == 0 and block->weak == 0)
        delete block;
    }
    block = nullptr;
  }
};

struct Value {
  int value;
  static int counter;
  Value(): value{counter++} { std::cout << "Value(static): " << value << '\n'; }
  Value(int v): value(v) { std::cout << "Value(init): " << value << '\n'; }
  ~Value() { std::cout << "Value(term): " << value << '\n'; }
};

std::ostream &operator<<(std::ostream &out, Value const &v) {
  return out << "Value { " << v.value << " }";
}

int Value::counter = 0;

void print(shared_ptr<Value> value) {
  std::cout << "*value: " << *value << '\n';
}

int main() {
  std::cout << std::boolalpha;
  shared_ptr<Value> v1 = new Value{5052};
  print(v1);
  weak_ptr<Value> w1 = v1;
  assert(v1.unique());
  if(shared_ptr<Value> v = w1.lock()) {
    std::cout << "from weak: " << *v << '\n';
    assert(v.use_count() == 2);
  } else
    std::cout << "from weak: (empty)\n";
  assert(v1.unique());
  v1.reset();
  if(auto v = w1.lock())
    std::cout << "from weak: " << *v << '\n';
  else
    std::cout << "from weak: (empty)\n";
  {
    shared_ptr<Value> v2 = new Value{345};
    print(v2);
    std::cout << "v2.use_count() = " << v2.use_count() << '\n';
    w1 = v2;
    auto v3 = w1.lock();
    std::cout << "v3.use_count() = " << v3.use_count() << '\n';
    std::cout << "w1.use_count() = " << w1.use_count() << '\n';
    std::cout << "w1.expired() = " << w1.expired() << '\n';
  }
  std::cout << "w1.use_count() = " << w1.use_count() << '\n';
  std::cout << "w1.expired() = " << w1.expired() << '\n';
}
