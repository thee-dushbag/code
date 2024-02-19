#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <stdlib.h>

int current, sleep_time;
volatile int inf_loop = 1;

void handler(int _signal) {
  printf("Caught[%d]: '%s'\n", _signal, strsignal(_signal));
  switch (_signal)
  {
  case SIGUSR1:
    sleep_time -= 1;
    break;
  case SIGUSR2:
    sleep_time += 1;
    break;
  case SIGALRM:
    inf_loop = 0;
    break;
  }
}


void catch_all(void (*handler)(int)) {
  // signal(SIGINT, handler);
  // signal(SIGTERM, handler);
  // signal(SIGCONT, handler);
  // signal(SIGSTOP, handler);
  signal(SIGUSR1, handler);
  signal(SIGUSR2, handler);
  signal(SIGALRM, handler);
}

void count_to(int const stop) {
  for (current = 1, sleep_time = 1; current <= stop; ++current) {
    printf("Current[%d]: %d/%d\n", sleep_time, current, stop);
    sleep(sleep_time);
  }
}

void fs_syscalls() {
  // int fd = creat("./ignore.txt", 0751);
  // write(fd, (const void *)"Hello\n World\0", 6);
  // close(fd);
  // mknod("mypipe", 020744, 0x0402);
  // int fd = creat("hey.ign", 0744);
  int fd = open("hey.ign", O_RDONLY);
  if (fd == -1) exit(2);
  char message[13];
  lseek(fd, -6, SEEK_END);
  int ar = read(fd, message, 12);
  printf("Amount: %d\n", ar);
  message[ar + 1] = '\0';
  // write(fd, "Hello World\n", 12);
  printf("Read Message: '%s'\n", message);
  close(fd);
}

int main(int argc, char **argv) {
  // fs_syscalls();
  // catch_all(handler);
  // printf("PID: %d\n", getpid());
  // count_to(50);
  // pause();
  // while(inf_loop);
  // puts("Done!");
}
