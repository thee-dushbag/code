#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int main(int argc, char **argv) {
  puts("Hello");
  int pid = fork();
  if (pid == 0)
    printf("From Child | PPID: %d | PID: %d\n", getppid(), getpid());
  else
    printf("From Parent | PID: %d | CPID: %d\n", getpid(), pid);
  puts("World");
}
