#ifndef _HI_CORE_H
# error "Do not include this directly, it has to be prepared before use."
#endif

void hello(const char *name) {
  printf("Hello %s, how was your day?\n", name);
}

int square(int this) {
  return this * this;
}

const char *status(int class) {
  if (class >= 100) return "RICH";
  else if (class >= 0) return "MIDDLE";
  else return "POOR";
}