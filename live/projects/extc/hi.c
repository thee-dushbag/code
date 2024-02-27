#include <stdio.h>
#include "hi/hi.h" // Include our core application.

// For some reason I cannot use getline, this utility will truly help
int mgetline(char *buffer, size_t size) {
  int idx = 0;
  for (char ch; (ch = getc(stdin)) != 10; ++idx)
    buffer[idx] = ch;
  return idx;
}

int main(int argc, char **argv) {
  char name[100];
  printf("Enter your name: ");
  mgetline(name, 99);
  hello(name);
  int class;
  printf("Enter a number between -200 to 500: ");
  scanf("%d", &class);
  if (class > 500 || class < -200) {
    fprintf(stderr, "Expected a number between -200 to 500 inclusive, but got %d\n", class);
    return 1;
  }
  printf("You are in the %s CLASS.\n", status(class));
  printf("%d * %d = %d\n", class, class, square(class));
}
