#include <threads.h>
#include <stdio.h>

#ifdef WTHRD
# define which_thrd(where) printf("Executing %s in thread id %#x\n", #where, thrd_current())
#else
# define which_thrd(where)
#endif

typedef struct {
  const char* name;
  int age : 8;
} Person;

void person_greet(Person* person) {
  which_thrd(person_greet);
  printf("Hello %s, you are %d years old.\n",
    person->name, person->age);
}

void person_init2(Person* person, const char* name, unsigned char age) {
  person->name = name;
  person->age = age;
}

void person_init(Person* person) {
  person_init2(person, NULL, 0);
}

Person person_init3() {
  Person person;
  person_init(&person);
  return person;
}

Person person_init4(const char* name, unsigned char age) {
  Person person;
  person_init2(&person, name, age);
  return person;
}

int greet_wrapper(void* person) {
  person_greet(person);
  return thrd_success;
}

int main() {
  which_thrd(main);
  auto me = person_init4("Simon Nganga", 21);
  thrd_t mt;
  thrd_create(&mt, greet_wrapper, &me);
  thrd_join(mt, NULL);
}
