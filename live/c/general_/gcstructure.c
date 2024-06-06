#include <stdio.h>
#include <stdint.h>

typedef union {
  uint64_t count;
  struct {
    uint32_t mem;
    uint32_t var;
  } ref;
} Count;

typedef struct {
  Count gc;
  long double value;
} Double;

#define _Rox_OPREF(v, _w, op) v.gc.ref._w op
#define Rox_INCREF(v, _w) _Rox_OPREF(v, _w, ++)
#define Rox_DECREF(v, _w) _Rox_OPREF(v, _w, --)

#define Rox_MemINCREF(v) Rox_INCREF(v, mem)
#define Rox_VarINCREF(v) Rox_INCREF(v, var)

#define Rox_MemDECREF(v) Rox_DECREF(v, mem)
#define Rox_VarDECREF(v) Rox_DECREF(v, var)

void print_count(Count t) {
  printf("Count(count=%lu, ref.mem=%u, ref.var=%u)",
    t.count, t.ref.mem, t.ref.var);
}

void print_double(Double d) {
  printf("Double(value=%llf, gc=", d.value);
  print_count(d.gc);
  puts(")");
}

int main(int argc, char** argv) {
  Double d = { 0, 3.141 };
  print_double(d);
  Rox_VarINCREF(d);
  print_double(d);
  d.value *= 3;
  print_double(d);
  Rox_VarDECREF(d);
  print_double(d);
}
