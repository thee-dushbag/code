#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void describe_errno(int const errno) {
  printf("%d: %s\n", errno, strerror(errno));
}

int main(int argc, char **argv) {
  for (int i = 1; i < argc; i++)
    describe_errno(atoi(argv[i]));
}

