#include <stdio.h>

#define NUMBER 100
#define print(expr) printf("%s = %d\n", #expr, expr)
#define reset(number) number = NUMBER

int main(int argc, char **argv) {
  int number;

  reset(number);
  print(++number);

  reset(number);
  print(number++);

  reset(number);
  print(--number);

  reset(number);
  print(number--);
}
