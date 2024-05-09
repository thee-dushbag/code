#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <endian.h>

#define PB_STEP_POLICY 1
#define PB_LOOP_POLICY 2
#ifndef PB_POLICY
# define PB_POLICY PB_LOOP_POLICY
#endif // PB_POLICY

#define _puintN_dec(N) \
  void puint ## N(uint ## N ## _t); \
  void puint ## N ## l(uint ## N ## _t)

_puintN_dec(64);
_puintN_dec(32);
_puintN_dec(16);
_puintN_dec(8);

#undef _puintN_dec

uint64_t to_int(double);
void inspect(double);
double to_double(uint64_t);
void print(const char*, uint64_t);
void pbyte(uint8_t);
void inspector();
void inspect_seq(int, int);
uint64_t zero = 0b0000000000000000000000000000000000000000000000000000000000000000;
uint64_t posinf = 0b0111111111110000000000000000000000000000000000000000000000000000;
uint64_t neginf = 0b1111111111110000000000000000000000000000000000000000000000000000;
uint64_t notanum = 0b0111111111111000000000000000000000000000000000000000000000000000;
uint64_t nnotnum = 0b1111111111111000000000000000000000000000000000000000000000000000;
uint64_t mfloat = 16473UL << 48; // 4636737291354636288 -> 100.0
const uint64_t
  sign_mask = 0x80'00'00'00'00'00'00'00,
  exp_mask = 0x7f'f0'00'00'00'00'00'00,
  val_mask = 0x00'0f'ff'ff'ff'ff'ff'ff;

int main(int argc, char** argv) {
  // inspect_seq(1, 513); return 0;
  inspector();
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

void inspector() {
  double number;
  for ( ;;) {
    printf("Enter a double: ");
    scanf("%lf", &number);
    inspect(number);
  }
}

void inspect(double val) {
  uint64_t num = *(uint64_t*)&val;
  uint16_t exp = (num & exp_mask) >> 52;
  uint64_t value = (num & val_mask);
  bool sign = num & sign_mask;
  printf("double: %lf\n", val);
  printf("  layout: ");
  puint64l(num);
  printf("  sign  : %s\n", sign ? "true" : "false");
  printf("  exp   : %u\n", exp);
  printf("    layout: ");
  puint16l(exp);
  printf("  value : %lu\n", value);
  printf("    layout: ");
  puint64l(value);
}

void _print_bits(uint8_t byte, uint8_t mask) {
  for (uint8_t b = 128; b; b >>= 1)
    if (b & mask) putchar((byte & b)? '1' : '0');
}

void _print_bytes(uint64_t bytes, uint64_t masks) {
  uint8_t
    *bits = (uint8_t *)&bytes,
    *msks = (uint8_t *)&masks;
  for (int b = 0; b < 8; b++)
    _print_bits(bits[b], msks[b]);
}

void _print_double(double number) {
  uint64_t value = *(uint64_t*)&number;
  _print_bytes(value, sign_mask);
  putchar('\'');
  _print_bytes(value, exp_mask);
  putchar('\'');
  _print_bytes(value, val_mask);
}

void inspect_seq(int start, int stop) {
  double num;
  for (; start < stop; start++) {
    num = start;
    printf("%lf\t", num);
    // _print_double(num);
    puint64(to_int(num));
    putchar('\n');
  }
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

void _print_little_order(uint8_t* bytes, size_t size, char sep) {
  _print_byte(bytes[--size]);
  for ( int idx = --size; idx >= 0; --idx ) {
    putchar(sep); _print_byte(bytes[idx]);
  }
}

void _print_big_order(uint8_t* bytes, size_t size, char sep) {
  _print_byte(bytes[0]);
  for ( size_t b = 1; b < size; ++b ) {
    putchar(sep); _print_byte(bytes[b]);
  }
}

void _print_layout(void* bytes, size_t size, char sep) {
  sep = sep == 0 ? '\'' : sep;
#if BYTE_ORDER == LITTLE_ENDIAN
  _print_little_order(bytes, size, sep);
#elif BYTE_ORDER == BIG_ENDIAN
  _print_big_order(bytes, size, sep);
#else
# error "Could not resolve byte order"
#endif
}

#define _intN_t(N) uint ## N ## _t
#define _pl_name(N) _print_int ## N ## _layout
#define _puintN_raw(N, S, L) \
  void puint ## S(_intN_t(N) number) \
  { _pl_name(N)(number, 0)L }

#define _print_intN_layout(N) \
  void _pl_name(N)(_intN_t(N) number, char sep) \
  { _print_layout(&number, (size_t)(N / 8), sep); }
#define _puintN(N) _puintN_raw(N, N, ;)
#define _puintNl(N) _puintN_raw(N, N ## l, ; putchar(10); )

#define _intN_lv(N) \
  _print_intN_layout(N) \
  _puintN(N) \
  _puintNl(N)

_intN_lv(64);
_intN_lv(32);
_intN_lv(16);
_intN_lv(8);

#undef _print_intN_layout
#undef _puintN_raw
#undef _intN_lv
#undef _pl_name
#undef _puintNl
#undef _puintN
#undef _intN_t

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
