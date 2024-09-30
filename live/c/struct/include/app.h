#pragma once

#ifndef PONE
# define PONE name
#endif

#ifndef PTWO
# define PTWO email
#endif

#ifndef PTHR
# define PTHR company
#endif

struct app_t {
  char PONE[30];
  char PTWO[30];
  char PTHR[30];
};

void app_print(struct app_t *);

void app_init(
  struct app_t *,
  const char *,
  const char *,
  const char *
);

#undef PONE
#undef PTWO
#undef PTHR
