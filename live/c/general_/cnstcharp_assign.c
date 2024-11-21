#include <stdio.h>

struct person {
  char name[50];
  int age;
  struct person *boss;
};


void print_person(struct person *p) {
  printf("Person(name='%s', age=%d, boss=%p)\n", p->name, p->age, p->boss);
}

int main() {
  struct person me = { .name = "Simon Nganga", .age = 22 };
  print_person(&me);
  print_person(&(struct person){ .name = "Jane Doe", .age = 11 });
  printf("sizeof(person) = %lu\n", sizeof(me));
}

