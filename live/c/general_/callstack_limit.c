#include <stdio.h>

/*
recursion limit for my machine
is around and above: 261700
*/

void test_limit(unsigned long last) {
  printf("Current: %ld\n", last);
  test_limit(last + 1);
}

int main(int argc, char **argv) {
  test_limit(1);
}
