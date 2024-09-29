#include <app.h>
#include <stdio.h>

void app_init() {
  printf("Engine running; Uber, ready to go.\n");
}

void app_notify() {
  printf("Uber getting to destination.\n");
}

void app_dinit() {
  printf("Checking user feedback. Uber shutting down.\n");
}

