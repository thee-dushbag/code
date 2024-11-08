#include <stdio.h>

typedef unsigned int uint;
typedef unsigned long ulong;

#define _ViewAS(var, type) (*(type *)&var)

#define _Caster(From, To)                                                      \
  To From##2##To(From var) { return _ViewAS(var, To); }

#define _Caster2(T1, T2) _Caster(T1, T2) _Caster(T2, T1)

_Caster2(uint, float);
_Caster2(ulong, double);

#define _PrintRange(T1, T2, S, F)                                              \
  void range_##T1##_##T2(T1 start, T1 end, T1 step) {                          \
    while (start < end) {                                                      \
      printf("0x%0." #S F "X = %.150" F "f\n", start, _ViewAS(start, T2));     \
      start += step;                                                           \
      if (start < step)                                                        \
        break;                                                                 \
    }                                                                          \
  }

_PrintRange(uint, float, 8, "");
_PrintRange(ulong, double, 16, "l");

#define MAX_FLOAT uint2float(0x7F7FFFFF)
#define MIN_FLOAT uint2float(0xFF7FFFFF)
#define MAX_DOUBLE ulong2double(0x7FEFFFFFFFFFFFFF)
#define MIN_DOUBLE ulong2double(0xFFEFFFFFFFFFFFFF)

#define INF_FLOAT uint2float(0x7F700000)
#define INF_FLOAT_ uint2float(0xFF700000)
#define INF_DOUBLE ulong2double(0x7FF0000000000000)
#define INF_DOUBLE_ ulong2double(0xFFF0000000000000)

#define NAN_FLOAT uint2float(0x7F800001)
#define NAN_FLOAT_ uint2float(0xFF800001)
#define NAN_DOUBLE ulong2double(0x7FF0000000000001)
#define NAN_DOUBLE_ ulong2double(0xFFF0000000000001)

#define PRINT(head, value) printf(#head ": %lf\n", value)
#define PRINTV(value) PRINT(value, value)

#define PMIN_FLOAT PRINT(Min Float, MIN_FLOAT)
#define PMAX_FLOAT PRINT(Max Float, MAX_FLOAT)
#define PMIN_DOUBLE PRINT(Min Double, MIN_DOUBLE)
#define PMAX_DOUBLE PRINT(Max Double, MAX_DOUBLE)
#define PINF_FLOAT PRINT(NaN Float, INF_FLOAT)
#define PINF_FLOAT_ PRINT(-NaN Float, INF_FLOAT_)
#define PINF_DOUBLE PRINT(NaN Double, INF_DOUBLE)
#define PINF_DOUBLE_ PRINT(-NaN Double, INF_DOUBLE_)
#define PNAN_FLOAT PRINT(NaN Float, NAN_FLOAT)
#define PNAN_FLOAT_ PRINT(-NaN Float, NAN_FLOAT_)
#define PNAN_DOUBLE PRINT(NaN Double, NAN_DOUBLE)
#define PNAN_DOUBLE_ PRINT(-NaN Double, NAN_DOUBLE_)

#define EXSTR(expr) #expr, expr

#define P754Details                                                            \
  PMIN_FLOAT;                                                                  \
  PMAX_FLOAT;                                                                  \
  PMIN_DOUBLE;                                                                 \
  PMAX_DOUBLE;                                                                 \
  PINF_FLOAT;                                                                  \
  PINF_FLOAT_;                                                                 \
  PINF_DOUBLE;                                                                 \
  PINF_DOUBLE_;                                                                \
  PNAN_FLOAT;                                                                  \
  PNAN_FLOAT_;                                                                 \
  PNAN_DOUBLE;                                                                 \
  PNAN_DOUBLE_

void prange();
void others();

int main() {
  printf("sizeof(long double) = %lu\n", sizeof(long double));
  printf("%s = 0x%0.8X\n", EXSTR(float2uint(1e10)));
  printf("%s = %.7ff\n", EXSTR(uint2float(0x501502F9)));
  printf("%s = 0x%0.8X\n", EXSTR(float2uint(-1e10)));
  printf("%s = %.7ff\n", EXSTR(uint2float(0xD01502F9)));
  printf("%s = %.7ff\n", EXSTR(uint2float(0x40400000)));

  printf("%s = %.7ff\n", EXSTR(uint2float(0x43960000)));
  printf("%s = 0x%0.8X\n", EXSTR(float2uint(0.32)));
  printf("%s = %.7ff\n", EXSTR(uint2float(0x3EA3D70B)));
  printf("%s = %.7ff\n", EXSTR(uint2float(0x3EA3D70A)));
  printf("%s = %.8lf\n", EXSTR(ulong2double(0x4020BCED916872B0)));
  printf("%s = 0x%0.16lX\n", EXSTR(double2ulong(100.0)));
  printf("%s = %.8lf\n", EXSTR(ulong2double(0x4059000000000000)));
  printf("%s = %.7ff\n", EXSTR(uint2float(0xC3480000)));
  printf("%s = %.8lf\n", EXSTR(ulong2double(0xC069000000000000)));
  // others();
  // prange();
}

void prange() {
  range_uint_float(0, 0xFFFFFFFF, 0x100000);
  putchar('\n');
  range_ulong_double(0, 0xFFFFFFFFFFFFFFFF, 0x10000000000000);
}

void others() {
  P754Details;
  PRINTV(uint2float(0x3FA8F5C2));
  PRINTV(uint2float(0x0051EB86));
  PRINTV(ulong2double(0x3FF51EB851EB851E));
  PRINTV(ulong2double(0x3FF8000000000000));
  PRINTV(MAX_DOUBLE + ulong2double(0x7FE0000000000001));
  PRINTV(MIN_DOUBLE + ulong2double(0xFFE0000000000001));
}
