#include <format>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <iterator>
#include <experimental/iterator>
#include <iomanip>
#include <tuple>
#include <span>

using person_tuple = std::tuple<std::string, std::string, uint>;

struct person {
  std::string name, email;
  uint age;
  person(std::string const& name, std::string const& email, uint const age)
    : name{ name }, email{ email }, age{ age } { }
  person(std::string&& name, std::string&& email, uint const age)
    : name{ std::move(name) }, email{ std::move(email) }, age{ age } { }
  person(person const& p)
    : name{ p.name }, email{ p.email }, age{ p.age } { }
  person(person&& p)
    : name{ std::move(p.name) },
    email{ std::move(p.email) },
    age{ p.age } { }
  person(person_tuple const& pt) noexcept {
    auto const& [n, e, a] = pt;
    name = n, email = e, age = a;
  }
  person(person_tuple&& pt) noexcept {
    auto&& [n, e, a] = std::move(pt);
    name = std::move(n), email = std::move(e), age = a;
  }
  std::string greet(std::string_view const& name)
    const noexcept {
    return (std::stringstream() << "Hello " << name
      << "? My name is " << this->name << "."
      ).str();
  }
  std::string greet(person const& p)
    const noexcept {
    return greet(p.name);
  }
  friend std::ostream&
    operator<<(std::ostream& out, person const& p)
    noexcept {
    return out << std::string(p);
  }
  operator std::string() const noexcept {
    return (std::stringstream() << "person(name='" << name
      << "', email='" << email
      << "', age=" << age << ')').str();
  }
  operator person_tuple() const noexcept {
    return { name, email, age };
  }
};

struct File : public std::stringstream {
  std::string file;
  bool closed;
  File() = delete;
  File(std::string const& file)
    : file{ file }, closed{ false } {
    std::cout << "Opening File: " << file << '\n';
  }
  virtual ~File() {
    close();
    std::cout << "+---------------------[ FILE CONTENT ]--------+\n";
    std::string content = this->str();
    std::cout << content << (content.back() == '\n' ? "" : "\n");
    std::cout << "+---------------------------------------------+\n";
  }
  void close() noexcept {
    if (closed) return;
    closed = true;
    std::cout << "Closing File: " << file << '\n';
  }
};

void print(person const& p) {
  std::cout << p << '\n';
}

void detail(std::string const& name, std::string const& email, uint age) {
  std::cout << std::setfill(' ')
    << "+-------+----------------[ PERSON ]----------+\n"
    << "| Name  | " << std::setw(35) << std::left << name << "|\n"
    << "| Email | " << std::setw(35) << std::left << email << "|\n"
    << "| Age   | " << std::setw(24) << std::right << age << " years old |\n"
    << "+--------------------------------------------+\n";
}

person create
(std::string const& name, std::string const& email, uint age) {
  return { name, email, age };
}

struct range {
  uint start, stop, step;
  range() = delete;
  range(uint stop) noexcept
    : start{ 0U },
    stop{ stop }, step{ 1U } { }
  range(uint start, uint stop) noexcept
    : start{ start },
    stop{ stop }, step{ 1U } { }
  range(uint start, uint stop, uint step)
    noexcept
    : start{ start },
    stop{ stop }, step{ step } { }
  void shift() noexcept {
    if (!done()) start += step;
  }
  bool done() const noexcept {
    return start >= stop;
  }
  uint value() const noexcept {
    return start;
  }
  uint size() const noexcept {
    return stop - start;
  }
};


template<typename T>
struct array {
  array() = default;
  array(std::size_t s)
    : size{ s } {
    allocate();
  }
  void allocate() noexcept {
    if (size == 0 || storage) return;
    store = new T[size];
    storage = true;
  }
  void deallocate() noexcept {
    if (!storage) return;
    storage = false;
    delete[] store;
    store = nullptr;
  }
  T* begin() const noexcept {
    return store;
  }

  T* end() const noexcept {
    return store ? store + size : nullptr;
  }

  T* rbegin() const noexcept {
    return end() - 1;
  }

  T* rend() const noexcept {
    return begin() - 1;
  }

  ~array() noexcept {
    deallocate();
  }
private:
  T* store{ nullptr };
  std::size_t size{ 0 };
  bool storage{ false };
};

struct iter_range {
  range _range;
  array<uint> store;
  iter_range() = delete;
  iter_range(range _range) noexcept
    : _range{ _range }, store{ _range.size() }
    { init(); }
  
  void init() noexcept {
    std::size_t cur { 0 };
    uint *a = store.begin();
    while(!_range.done()) {
      a[cur] = _range.value();
      _range.shift();
      cur ++;
    }
  }

  auto begin()
  { return std::reverse_iterator(store.end()); }
  auto end()
  { return std::reverse_iterator(store.begin()); }
};

template<typename Derived>
struct IncrementMixin {
  Derived &operator++()
  { return increment(); }
  Derived &operator++(int)
  { return increment(); }
  Derived &operator--()
  { return decrement(); }
  Derived &operator--(int)
  { return decrement(); }
private:
  Derived& increment(int value = 1) {
    Derived &tmp = static_cast<Derived&>(*this);
    tmp.setValue(tmp.getValue() + value);
    return tmp;
  }
  Derived& decrement(int value = 1) {
    Derived &tmp = static_cast<Derived&>(*this);
    tmp.setValue(tmp.getValue() - value);
    return tmp;
  }
};

// struct IncrementThisMixin {
//   auto &operator++(this auto& self)
//   { return increment(self); }
//   auto &operator++(this auto& self, int)
//   { return increment(self); }
//   auto &operator--(this auto& self)
//   { return decrement(self); }
//   auto &operator--(this auto& self, int)
//   { return decrement(self); }
// private:
//   auto& increment(auto &tmp, int value = 1) {
//     // auto &tmp = static_cast<auto&>(*this);
//     tmp.setValue(tmp.getValue() + value);
//     return tmp;
//   }
//   auto& decrement(auto &tmp, int value = 1) {
//     // auto &tmp = static_cast<auto&>(*this);
//     tmp.setValue(tmp.getValue() - value);
//     return tmp;
//   }
// };


struct Counter: IncrementMixin<Counter> {
  Counter(int v): value { v } { }
  Counter() : value { 0 } { }
  int getValue() const noexcept 
  { return value; }
  void setValue(int v) noexcept
  { value = v; }
  int operator*() const noexcept
  { return getValue(); }
  friend std::ostream &
  operator<<(std::ostream &out, Counter const &c)
  { return out << "Counter(" << c.value << ')'; }
  operator int() const noexcept
  { return value; }

private:
  int value;
};

struct Age: IncrementMixin<Age> {
  Age(int v): age { v } { }
  Age() : age { 0 } { }
  int getValue() const noexcept 
  { return age; }
  void setValue(int v) noexcept
  { age = v; }
  int operator*() const noexcept
  { return getValue(); }
  friend std::ostream &
  operator<<(std::ostream &out, Age const &c)
  { return out << "Age(" << c.age << ')'; }
  operator int() const noexcept
  { return age; }

private:
  int age;
};

auto main(int argc, char** argv) -> int {
  std::vector<person_tuple> people{
    {"Simon Nganga", "simongash@gmail.com", 21},
    {"Faith Njeri", "faithnjeri@outlook.com", 11},
    {"Lydia Wanjiru", "lydiawanjiru@gmail.com", 38},
    {"Dairus Kimani", "dariuskipesa@yahoo.mail", 25},
    {"Dennis Losuru", "dennislosuru@thumderbird.com", 24},
    {"Harrison Kariuki", "harrykariks@yahoo.com", 19}
  };

  for(Age c; *c != 10; c++)
    std::cout << "Current at: " << c << '\n';


  // range r { 1, 10 };

  // for (uint const &i : iter_range(r))
  //   std::cout << "Current at: " << i << '\n';



  // File outfile{ "hello.txt" };
  // std::for_each(
  //   std::cbegin(people),
  //   std::cend(people),
  //   [](person_tuple const& pt) { std::apply(detail, pt); }
  // );

  // for (auto const& pt : people)
  //   std::apply(detail, pt);

  // std::cout << "\n\n";

  // for (auto iter = people.crbegin();
  //   iter != people.crend(); iter++
  //   )
  //   std::apply(detail, *iter);

  // person_tuple me = people[0];
  // std::apply(detail, me);

  // outfile << "Hello World\nMy name is Simon Nganga.\nI am 21 years old.\n";
  // outfile.close();
  // std::cout << "Other Ops.....\n";
  // outfile.close();
}