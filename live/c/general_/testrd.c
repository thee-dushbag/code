#include <stdio.h>
#include "snn_utils.h"

void sum(void *a, void *b)
{ *((int *)a) = *((int *)a) + *((int *)b); }

int main(int argc, char **argv) {
  int arr[5] = { 1, 2, 3, 4, 5 };
  int accum = 0;
  snn_reduce(arr, sizeof(int), 5, &accum, sum);
  printf("1 + 2 + 3 + 4 + 5 = %d\n", accum);
}
