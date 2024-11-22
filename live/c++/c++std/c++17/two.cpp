#include <iostream>
#include <memory>
#include <string>

using std::cout;

struct Person : std::enable_shared_from_this<Person> {
  std::string name;
  int age;
};

struct Value {
  int value;
  static int counter;
  Value(): value{counter++} { cout << "Value(static): " << value << '\n'; }
  Value(int v): value(v) { cout << "Value(init): " << value << '\n'; }
  ~Value() { cout << "Value(term): " << value << '\n'; }
};

std::ostream &operator<<(std::ostream &out, Value const &v) {
  return out << "Value { " << v.value << " }";
}

int Value::counter = 0;

template <typename T>
struct Node {
  T value;
  std::shared_ptr<Node> next;
};

struct ShareMe: std::enable_shared_from_this<ShareMe> {
  std::shared_ptr<ShareMe> share() {
    return shared_from_this();
  }
};

int main() {
  std::shared_ptr<Value> v;
  cout << *v << '\n';
  return 0;
  Node<Value> base{10};
  base.next = std::make_shared<Node<Value>>(20);
  base.next->next = std::make_shared<Node<Value>>(30);
  auto start = base;
  for(;;) {
    cout << '\t' << start.value << '\n';
    if(start.next)
      start = *start.next;
    else
      break;
  }
  base.next->next->next = base.next; // memory leak
  return 0;
  cout << std::boolalpha;
  int numbers[10];
  Value *values = (Value *)numbers;
  for(int i = 0; i < 10; i++)
    ::new(values + i) Value{i};
  int sum = 0;
  for(int i = 0; i < 10; i++) {
    sum += (values + i)->value;
    cout << "numbers[" << i << "] == values[" << i
         << "].value = " << (numbers[i] == values[i].value) << '\n';
  }
  cout << "sum: " << sum << '\n';
  for(int i = 9; i >= 0; i--)
    (values + i)->~Value();
  // Value values[10]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
  /*Person me{ "Simon Nganga", 23 };*/
}
