#include <stdio.h>

int main(int argc, char **argv) {
    printf("C: Hello World\n");
    int end = 10'000'000;
    for(int i = 0; i < end; i++)
        printf("\rC: Line %d", i);
    printf("\rC: Done.... %d\n", end);
}