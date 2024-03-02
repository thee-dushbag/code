#include <iostream>

struct A;
struct B;

struct C {                                  };
struct B { void operator+(A const &) const; };
struct A { void operator+(B const &) const; };

void A::operator+(B const &) const
{ std::cout << "A::operator+(B const &)\n"; }

void B::operator+(A const &) const
{ std::cout << "B::operating+(A const &)\n"; }

void operator+(C const &, A const &)
{ std::cout << "operator+(C const &, A const &)\n"; }

void operator+(A const &, C const &)
{ std::cout << "operator+(A const &, C const &)\n"; }

int main() {
	A a;
	B b;
	C c;
	a + b;
	b + a;
	c + a;
	a + c;
}

