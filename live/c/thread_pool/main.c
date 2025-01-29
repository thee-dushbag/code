#include "pool.h"
#include <stdio.h>
#include <threads.h>

void greet(const char *name, unsigned count, struct timespec period) {
  for (; count; count--) {
    printf("%d: Hello %s?\n", count, name);
    thrd_sleep(&period, NULL);
  }
  printf("Goodbye %s!!!\n", name);
}

int factorial(int n) { return n ? n * factorial(n - 1) : 1; }

struct factorial_args {
  int n, result;
};

void factorial_function(void *args) {
  struct factorial_args *fargs = (struct factorial_args *)args;
  fargs->result = factorial(fargs->n);
}

struct greet_args {
  const char *name;
  unsigned count;
  struct timespec period;
};

void greet_function(void *args) {
  struct greet_args *pack = (struct greet_args *)args;
  greet(pack->name, pack->count, pack->period);
}

#define create_task(NAME, COUNT, SECS)                                         \
  (task_t) {                                                                   \
    .arg = &(struct greet_args){.name = NAME,                                  \
                                .count = COUNT,                                \
                                .period = (struct timespec){0, 500000000}},    \
    .function = greet_function                                                 \
  }

int main() {
  struct pool_t pool;
  struct factorial_args fargs = {.n = 12, .result = 0};
  task_t factorial_task = {.arg = &fargs, .function = factorial_function};
  pool_init(&pool, 4);
  pool_push(&pool, &create_task("Joan Megatron      [1]", 5, 1));
  pool_push(&pool, &create_task("Simon Brooks     [1]", 7, 1));
  pool_push(&pool, &create_task("Anne Megatron      [1]", 6, 1));
  pool_push(&pool, &create_task("Bernard Keehl    [1]", 4, 1));
  pool_push(&pool, &create_task("David Lorein    [1]", 6, 1));
  pool_push(&pool, &create_task("Joan Megatron      [2]", 5, 1));
  pool_push(&pool, &factorial_task);
  pool_push(&pool, &create_task("Simon Brooks     [2]", 7, 1));
  pool_push(&pool, &create_task("Anne Megatron      [2]", 6, 1));
  pool_push(&pool, &create_task("Bernard Keehl    [2]", 4, 1));
  pool_push(&pool, &create_task("David Lorein    [2]", 6, 1));
  pool_push(&pool, &create_task("Joan Megatron      [3]", 5, 1));
  pool_push(&pool, &create_task("Simon Brooks     [3]", 7, 1));
  pool_push(&pool, &create_task("Anne Megatron      [3]", 6, 1));
  pool_push(&pool, &create_task("Bernard Keehl    [3]", 4, 1));
  pool_push(&pool, &create_task("David Lorein    [3]", 6, 1));
  pool_destroy_wait(&pool);
  printf("factorial(%d) = %d\n", fargs.n, fargs.result);
}

