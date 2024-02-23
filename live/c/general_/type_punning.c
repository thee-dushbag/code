#include <stdio.h>

typedef enum {
  PERSON,
  EMPLOYEE,
  BUILDING
} Type;

typedef struct {
  int national_id;
  const char *name;
  const char *email;
} Person;

typedef struct {
  const char *job;
  const char *company;
  Person info;
} Employee;

typedef struct {
  int stories;
  const char *name;
  const char *street;
  Person owner;
} Building;

typedef struct {
  Type type;
  union {
    Person person;
    Employee employee;
    Building building;
  } as;
} ObjectType;

#define EMPLOYEE_OBJ(value) \
  ((ObjectType){ .type = EMPLOYEE, .as.employee = (value) })
#define BUILDING_OBJ(value) \
  ((ObjectType){ .type = BUILDING, .as.building = (value) })
#define PERSON_OBJ(value) \
  ((ObjectType){ .type = PERSON, .as.person = (value) })

void _person_print(Person *person) {
  printf("ID: %d\n", person->national_id);
  printf("Name: %s\n", person->name);
  printf("Email: %s\n", person->email);
}

void _employee_print(Employee *emp) {
  _person_print(&emp->info);
  printf("Company: %s\n", emp->company);
  printf("Job: %s\n", emp->job);
}

void _building_print(Building *building) {
  _person_print(&building->owner);
  printf("Stories: %d\n", building->stories);
  printf("BuildingName: %s\n", building->name);
  printf("Street: %s\n", building->street);
}

void person_print(Person *person) {
  printf("-------------[ PERSON ]-------------\n");
  _person_print(person);
  printf("------------------------------------\n");
}

void employee_print(Employee *emp) {
  printf("------------[ EMPLOYEE ]------------\n");
  _employee_print(emp);
  printf("------------------------------------\n");
}

void building_print(Building *building) {
  printf("------------[ BUILDING ]------------\n");
  _building_print(building);
  printf("------------------------------------\n");
}

void person_init(
  Person *person,
  int id,
  const char *name,
  const char *email
) {
  *person = (Person){
    .national_id = id,
    .name = name,
    .email = email
  };
}

void employee_init(
  Employee *emp,
  Person info,
  const char *company,
  const char *job
) {
  *emp = (Employee){
    .company = company,
    .job = job,
    .info = info
  };
}

void building_init(
  Building *building,
  Person owner,
  int stories,
  const char *name,
  const char *street
) {
  *building = (Building){
    .name = name,
    .owner = owner,
    .street = street,
    .stories = stories
  };
}

Person person_create(
  int id,
  const char *name,
  const char *email
) {
  Person person;
  person_init(&person, id, name, email);
  return person;
}

Employee employee_create(
  Person info,
  const char *company,
  const char *job
) {
  Employee employee;
  employee_init(&employee, info, company, job);
  return employee;
}

Building building_create(
  Person owner,
  int stories,
  const char *name,
  const char *street
) {
  Building building;
  building_init(
    &building,
    owner,
    stories,
    name,
    street
  );
  return building;
}

Employee employee_create2(
  int id,
  const char *name,
  const char *email,
  const char *company,
  const char *job
) {
  return employee_create(
    person_create(id, name, email),
    company, job);
}

void _object_print(ObjectType *object) {
  switch (object->type) {
  case PERSON: person_print(&object->as.person);       break;
  case EMPLOYEE: employee_print(&object->as.employee); break;
  case BUILDING: building_print(&object->as.building); break;
  default: printf("Unknown object type: %d\n", object->type);
  }
}

void object_print(ObjectType *objects, size_t length) {
  for (size_t idx = 0; idx < length; ++idx)
    _object_print(objects + idx);
}

int main(int argc, char **argv) {
  Person me;
  person_init(&me, 5052, "Simon Nganga", "simongash@gmail.com");
  Employee alsome;
  puts("Two objects of type person and employee in their own variables.");
  employee_init(&alsome, me, "Google Inc.", "Software Engineer");
  person_print(&me);
  employee_print(&alsome);
  puts("\nBelow is an array with 3 different types of objects in it.");
  ObjectType p[] = {
    PERSON_OBJ(
      person_create(
        3456,
        "Simon",
        "simon@gmail.com"
      )
    ),
    EMPLOYEE_OBJ(
      employee_create2(
        5678,
        "Faith",
        "faith@gmail.com",
        "Microsoft",
        "Accoutant"
      )
    ),
    BUILDING_OBJ(
      building_create(
        person_create(
          87645,
          "Lydia",
          "lydia@gmail.com"
          ),
        4,
        "Njeri's Palace",
        "Kenyatta Avenue"
      )
    )
  };
  object_print(p, 3);
}
