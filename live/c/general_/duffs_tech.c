#include <stdio.h>
#include <stdbool.h>

#define BLOCK(value) {              \
    printf("This Block Prints:\n"); \
    printf("  '%s'\n", #value);       \
    printf("End of Block.\n");      \
  }

inline void
print_a() BLOCK(PRINT A)
inline void
print_b() BLOCK(PRINT B)

void for_each(void* start, void *end, size_t size, void (*callback)(void*)) {
  // for (; start != end; start += size) callback(start);
  while ( start != end ) start += (callback(start), size);
}

#define psize(type) printf("sizeof(%s) = %d\n", #type, sizeof(type))
#define ptsize(type) psize(type); psize(type*)

struct mytype {
  int a;
  double b;
  const char* c;
};

typedef struct mytype(*InitMyType)(int, double, const char*);

struct mytype init(
  int,
  double,
  const char*
) { }

enum BOOL { FALSE = 0, TRUE = 1 };
typedef enum BOOL BOOL;

typedef unsigned short uint8_t;

int square(int number) { return number * number; }

void psqr(int *n) { printf("%d * %d = %d\n", *n, *n, square(*n)); }

void vpsqr(void *ptr) { psqr((int *)ptr); }

int main(int argc, char** argv) {
  int numbers[] = { 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1 };
  for_each(numbers, numbers + 11, sizeof(int), vpsqr);

  // return 0;
  int age = 21;
  // uint8_t addr = (uint8_t)&age;
  int* ptr_age = &age;
  printf("Age = %d\n", age);
  // *((int *)addr) = 30;
  *ptr_age = 30;
  printf("Age = %d\n", age);
  int n = 3;
  switch(true) while(--n) {
    case false: BLOCK(CASE FALSE);
    default: BLOCK(DEFAULT WHILE);
  }
  // InitMyType hey = init;
  ptsize(int);
  ptsize(char);
  ptsize(float);
  ptsize(double);
  ptsize(char*);
  ptsize(const int);
  ptsize(InitMyType);
  ptsize(struct mytype);
}
