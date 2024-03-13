#include <stdio.h>

#define arg_function(arg_name) \
  int arg_name(int value) {    \
    printf("Reading %s: %d\n", \
      #arg_name, value);       \
    return value;              \
  }

arg_function(arg_a);
arg_function(arg_b);
arg_function(arg_c);

int add(int a, int b, int c) {
  return a + b + c;
}

int main(int argc, char** argv) {
  printf("Result: %d\n",
    add(arg_a(1), arg_b(2), arg_c(3))
  );
}
