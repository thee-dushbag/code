#ifndef _HI_H
#define _HI_H

// identifiers this and class are normal variable names
// in C hence the code below in correct from C while
// syntactically and semantically incorrect from C++ POV

#include <stdio.h>

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

#endif //_HI_H
