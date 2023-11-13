#include <stdio.h>

typedef struct {
  const char *name;
  unsigned short age;
} person;

void person_init(person *p, const char *name, unsigned short age) {
  p->name = name;
  p->age = age;
}

void person_print(person const *p) {
  printf("+---------+------------[ PERSON ]-------------+\n");
  printf("| Name    | %-33s |\n", p->name);
  printf("| Age     | %+30uyrs |\n", p->age);
  printf("+---------+-----------------------------------+\n");
}

int main(int argc, char **argv) {
  person poeple[10];
  char *names[10] = {"Simon", "Darius", "Faith", "Lydia", "Obed", "Dennis", "Nganga", "Wanjiru", "Njeri", "Samuel"};
  int ages[10] = {21, 25, 11, 38, 22, 23, 30, 27, 24, 47};
  for(short i = 0; i < 10; i++) person_init(poeple + i, names[i], ages[i]);
  for(short i = 0; i < 10; i++) person_print(poeple + i);
}