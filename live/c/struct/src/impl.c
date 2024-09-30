#include <app.h>
#include <string.h>
#include <stdio.h>

void app_print(struct app_t *ptr) {
  printf("+---------+--------------------------------+\n");
  printf("| Name    | %-30s |\n", ptr->name);
  printf("| Email   | %-30s |\n", ptr->email);
  printf("| Company | %-30s |\n", ptr->company);
  printf("+---------+--------------------------------+\n");
}

void app_init(
    struct app_t *ptr,
    const char *name,
    const char *email,
    const char *company ) {
  memcpy(ptr->name, name, 30);
  memcpy(ptr->email, email, 30);
  memcpy(ptr->company, company, 30);
}

