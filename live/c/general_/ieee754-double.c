#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <endian.h>

#define PB_STEP_POLICY 1
#define PB_LOOP_POLICY 2
#ifndef PB_POLICY
# define PB_POLICY PB_LOOP_POLICY
#endif // PB_POLICY

uint64_t to_int(double);
double to_double(uint64_t);
void print(const char*, uint64_t);
void puint64(uint64_t);
void puint64l(uint64_t);
void pbyte(uint8_t);

uint64_t zero = 0b0000000000000000000000000000000000000000000000000000000000000000;
uint64_t posinf = 0b0111111111110000000000000000000000000000000000000000000000000000;
uint64_t neginf = 0b1111111111110000000000000000000000000000000000000000000000000000;
uint64_t notanum = 0b0111111111111000000000000000000000000000000000000000000000000000;
uint64_t nnotnum = 0b1111111111111000000000000000000000000000000000000000000000000000;
uint64_t mfloat = 16473UL << 48; // 4636737291354636288 -> 100.0

int main(int argc, char** argv) {
  int value = 5052;
  uint64_t addr = (uint64_t)&value;
  printf("Value: %d\n", *((int*)addr));
  printf("Addr: ");
  puint64l(addr);
  // uint64_t a = to_int(-100), b = to_int(0.1), c = to_int(0.01), d = to_int(0.001);
  // print("a", a);
  // puint64l(a);
  // print("b", b);
  // puint64l(b);
  // print("c", c);
  // puint64l(c);
  // print("d", d);
  // puint64l(d);
  print("PositiveInf", posinf);
  print("NegativeInf", neginf);
  print("NaN", notanum);
  print("NegNaN", nnotnum);
  print("MyConstant", mfloat);
  print("Zero", zero);
  double nand = to_double(notanum);
  printf("(nan == nan) = %s\n",
    (nand == nand) ? "true" : "false");
  print("Pi", to_int(3.14));
}

void _print_byte(uint8_t number) {
#ifdef PB_PRINT_BYTE
  printf("(%d=", number);
#endif // PB_PRINT_BYTE
#if PB_POLICY == PB_STEP_POLICY
# define _1 0b00000001 // 1 << 0
# define _2 0b00000010 // 1 << 1
# define _3 0b00000100 // 1 << 2
# define _4 0b00001000 // 1 << 3
# define _5 0b00010000 // 1 << 4
# define _6 0b00100000 // 1 << 5
# define _7 0b01000000 // 1 << 6
# define _8 0b10000000 // 1 << 7
  putchar((number & _8) ? '1' : '0');
  putchar((number & _7) ? '1' : '0');
  putchar((number & _6) ? '1' : '0');
  putchar((number & _5) ? '1' : '0');
  putchar((number & _4) ? '1' : '0');
  putchar((number & _3) ? '1' : '0');
  putchar((number & _2) ? '1' : '0');
  putchar((number & _1) ? '1' : '0');
# undef _1
# undef _2
# undef _3
# undef _4
# undef _5
# undef _6
# undef _7
# undef _8
#elif PB_POLICY == PB_LOOP_POLICY
  for ( uint8_t b = 128; b; b >>= 1 )
    putchar((b & number) ? '1' : '0');
#endif // PB_POLICY ==
#ifdef PB_PRINT_BYTE
  putchar(')');
#endif // PB_PRINT_BYTE
}

void pbyte(uint8_t byte) {
  _print_byte(byte);
  putchar(10);
}

void _print_little_order(uint8_t* bytes, char sep) {
  _print_byte(bytes[7]);
  for ( int b = 6; b >= 0; b-- ) {
    putchar(sep); _print_byte(bytes[b]);
  }
}

void _print_big_order(uint8_t* bytes, char sep) {
  _print_byte(bytes[0]);
  for ( int b = 1; b <= 7; b++ ) {
    putchar(sep); _print_byte(bytes[b]);
  }
}

void _print_int_layout(uint64_t number) {
  uint8_t* bytes = (uint8_t*)&number;
  char separator = 39;
#if BYTE_ORDER == LITTLE_ENDIAN
  _print_little_order(bytes, separator);
#elif BYTE_ORDER == BIG_ENDIAN
  _print_big_order(bytes, separator);
#else
# error "Could not resolve byte order"
#endif
}

void puint64(uint64_t number) {
  _print_int_layout(number);
}

void puint64l(uint64_t number) {
  _print_int_layout(number);
  putchar(10);
}

void print(const char* name, uint64_t number) {
  printf("%-16s[%19ld]: %.6lf\n", name, number, to_double(number));
}

uint64_t to_int(double value) {
#ifdef CAST_TYPE
  return *((uint64_t*)&value);
#else
  uint64_t number;
  memcpy(&number, &value, sizeof(double));
  return number;
#endif // CAST_TYPE
}

double to_double(uint64_t value) {
#ifdef CAST_TYPE
  return *((double*)&value);
#else
  double number;
  memcpy(&number, &value, sizeof(uint64_t));
  return number;
#endif // CAST_TYPE
}
