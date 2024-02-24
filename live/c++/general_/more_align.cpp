#include <iostream>
#include <bitset>

class One {
  int one;
public:
  int get_one() const { return one; }
  void set_one(int val) { one = val; }
};

#ifdef PACK
# define ATTR_PACK __attribute__((packed))
#else
# define ATTR_PACK
#endif

// Packs neatly into 12 bytes
struct ATTR_PACK Pack {
  int a; // 4 bytes
  int b; // 4 bytes
  int c; // 4 bytes
}; // Total 12 bytes


struct ATTR_PACK Pack2 {
  int a;  // 4 bytes
  // Padding 4 bytes 0 if packed
  long b; // 8 bytes
}; // Total 16 bytes 12 if packed

struct ATTR_PACK Pack3 {
  long a; // 8 bytes
  int b;  // 4 bytes
  // Padding 4 bytes 0 if packed
}; // Total 16 bytes 12 if packed

struct ATTR_PACK Pack4 {
  long a; // 8 bytes
  int b;  // 4 bytes
  int c;  // 4 bytes
}; // Total 16 bytes


struct ATTR_PACK Pack5 {
  int a;  // 4 bytes
  long b; // 8 bytes
  // Padding 4 bytes 0 if packed
  int c;  // 4 bytes
}; // Total 16 bytes

std::ostream &operator<<(std::ostream &out, Pack const &p) {
  return out << "Pack{ a=" << p.a << ", b=" << p.b << ", c=" << p.c << " }";
}
std::ostream &operator<<(std::ostream &out, Pack2 const &p) {
  return out << "Pack2{ a=" << p.a << ", b=" << p.b << " }";
}
std::ostream &operator<<(std::ostream &out, Pack3 const &p) {
  return out << "Pack3{ a=" << p.a << ", b=" << p.b << " }";
}
std::ostream &operator<<(std::ostream &out, Pack4 const &p) {
  return out << "Pack4{ a=" << p.a << ", b=" << p.b << ", c=" << p.c << " }";
}

std::ostream &operator<<(std::ostream &out, Pack5 const &p) {
  return out << "Pack5{ a=" << p.a << ", b=" << p.b << ", c=" << p.c << " }";
}

void set(Pack *pack, int a, int b, int c) {
  int *blob = (int *)pack;
  *(blob + 0) = a;
  *(blob + 1) = b;
  *(blob + 2) = c;
}

void set(Pack2 *pack, int a, long b) {
  int *blob = (int *)pack;
  *blob = a;
#ifdef PACKED
  blob += 1;
#else
  blob += 2;
#endif
  *(long *)blob = b;
}

void set(Pack3 *pack, long a, int b) {
  long *blob = (long *)pack;
  *blob = a;
  blob += 1;
  *(int *)blob = b;
}

void set(Pack4 *pack, long a, int b, int c) {
  int *blob = (int *)pack;
  *(long *)blob = a;
  blob += 2;
  *(int *)blob = b;
  blob += 1;
  *(int *)blob = c;
}

void set(Pack5 *pack, int a, long b, int c) {
  int *blob = (int *)pack;
  *blob = a;
#ifdef PACKED
  blob += 1;
#else
  blob += 2;
#endif
  *(long *)blob = b;
  blob += 2;
  *(int *)blob = c;
}

class Two {
  int pri;
public:
  int pub;
  void set(int p) { pri = p; }
  int get() const { return pri; }
};

// Try to remove the padding
class Person {
  // Private attributes
  int age;
  std::string name;
public:
  Person(std::string const &name, int age)
    : age{ age }, name{ name } { }
  // Only getters and no setters
  std::string const &get_name()
    const {
    return name;
  }
  int get_age()
    const {
    return age;
  }
};

// Setting private fields from non-friend/method functions: set_name and set_age
void set_name(Person const &person, std::string const &name) {
  int *age = (int *)&person;
  age += 2; // Step to the next integer, which will
  // be the address of the name property.
  // Why 2? Also to skip the padding done by hardware/os
  // so that every variable can fit into a block of memory
  // which is a whole 8 bytes where an integer is only 4 bytes
  // therefore we skip by two integers to get to the address where
  // name is stored
  std::string *name_ptr = (std::string *)age; // Now age is the address of a std::string
  *name_ptr = name;
}

// By manipulating pointers and casting them from one type to another
// we can access any field and change its values
void set_age(Person const &person, int age) {
  int *age_ptr = (int *)&person;
  *age_ptr = age;
}

// Helper function to change both private fields
// name and age of a const declared Person object. Cool!
void set(Person const &person, std::string const &name, int age) {
  set_name(person, name);
  set_age(person, age);
}

#define P(expr)  std::cout << #expr << ": " << expr << '\n'
#define L std::cout << "--------------------------------\n"

auto main(int argc, char **argv) -> int {
  std::cout << std::boolalpha;
  P(sizeof(int));
  P(sizeof(long));
  P(sizeof(Pack));
  P(sizeof(Pack2));
  P(sizeof(Pack3));
  P(sizeof(Pack4));
  P(sizeof(Pack5));
  L;
  int a=10, b=20, c=30;
  Pack p;
  Pack2 p2;
  Pack3 p3;
  Pack4 p4;
  Pack5 p5;
  set(&p, a, b, c);
  set(&p2, a, b);
  set(&p3, a, b);
  set(&p4, a, b, c);
  set(&p5, a, b, c);
  P(p);
  P(p2);
  P(p3);
  P(p4);
  P(p5);
  L;
  Person me{ "Simon Nganga", 22 };
  P(me.get_name());
  P(me.get_age());
  set(me, "Faith Njeri", 12);
  P(me.get_name());
  P(me.get_age());
  L;
  int data{ 5052 };
  One *one = (One *)&data;
  P(one->get_one());
  data = 1000;
  P(one->get_one());
  One two;
  two.set_one(10);
  int *tdata = (int *)&two;
  L;
  P(two.get_one());
  P(*tdata);
  two.set_one(20);
  P(two.get_one());
  P(*tdata);
  *tdata = 30;
  P(two.get_one());
  P(*tdata);
  L;
  Two t;
  t.pub = 10;
  // t.pri = 20;
  t.set(20);
  int *d = (int *)&t;
  P(t.get());
  P(t.pub);
  *d = 30;
  *(d + 1) = 40;
  P(t.get());
  P(t.pub);
  L;
  int const age = 90;
  P(age);
  int *age_ptr = (int *)&age;
  P(*age_ptr);
  P(&age);
  P(age_ptr);
  age_ptr += 1;
  *(age_ptr - 1) = 110;
  P(age);
  L;
  int const var = 560;
  P(var);
  One *o = (One *)&var;
  o->set_one(456);
  P(var);
}
