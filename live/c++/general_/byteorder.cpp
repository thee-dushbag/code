#include <limits>
#include <cstdint>
#include <endian.h>
#include <iostream>

#define LINE "-----------------"

#define LLINE LINE "[ "
#define RLINE " ]" LINE

#define print(thing) \
  std::cout << #thing << " = " << thing << '\n'

#define psection(title) \
  std::cout << '\n' << LLINE << #title << RLINE << '\n'

#define plimits(itype) \
  print(std::numeric_limits<itype>::max()); \
  print(std::numeric_limits<itype>::min())

#define plimits_t(itype, type) \
  print((type)std::numeric_limits<itype>::max()); \
  print((type)std::numeric_limits<itype>::min())

#define plimits_ch(itype) plimits_t(itype, short)

#define psize(type) print(sizeof(type))

auto main(int argc, char **argv) -> int {
  std::cout << std::boolalpha;
  psection(Characters);
  print((uint8_t)0x41); // A
  print((uint8_t)0x42); // B
  print((uint8_t)0x43); // C
  print((uint8_t)0x44); // D
  print((uint8_t)0x45); // E
  print((uint8_t)0x46); // F
  print((uint8_t)0x47); // G
  print((uint8_t)0x48); // H

  const uint64_t offset = 0x41'42'43'44'45'46'47'48; // A,B,C,D,E,F,G,H
  uint8_t *offsets = (uint8_t *)&offset; // array made of 8 bytes, (64 / 8)

  psection(Endian and Byte order);
  print(BYTE_ORDER);
  print(LITTLE_ENDIAN);
  print(BIG_ENDIAN);

  psection(Unpack Offsets);
#if BYTE_ORDER == BIG_ENDIAN
  print(offsets[0]); // A
  print(offsets[1]); // B
  print(offsets[2]); // C
  print(offsets[3]); // D
  print(offsets[4]); // E
  print(offsets[5]); // F
  print(offsets[6]); // G
  print(offsets[7]); // H
  uint8_t
    A = (offset >>  0) & 0xff,
    B = (offset >>  8) & 0xff,
    C = (offset >> 16) & 0xff,
    D = (offset >> 24) & 0xff,
    E = (offset >> 32) & 0xff,
    F = (offset >> 40) & 0xff,
    G = (offset >> 48) & 0xff,
    H = (offset >> 56) & 0xff;
  // The most significant byte goes first in the array
  uint8_t space[8]{ A, B, C, D, E, F, G, H };
#elif BYTE_ORDER == LITTLE_ENDIAN
  print(offsets[7]); // A
  print(offsets[6]); // B
  print(offsets[5]); // C
  print(offsets[4]); // D
  print(offsets[3]); // E
  print(offsets[2]); // F
  print(offsets[1]); // G
  print(offsets[0]); // H
  uint8_t
    H = (offset >>  0) & 0xff,
    G = (offset >>  8) & 0xff,
    F = (offset >> 16) & 0xff,
    E = (offset >> 24) & 0xff,
    D = (offset >> 32) & 0xff,
    C = (offset >> 40) & 0xff,
    B = (offset >> 48) & 0xff,
    A = (offset >> 56) & 0xff;
  // The most significant byte is the last in the array
  uint8_t space[8]{ H, G, F, E, D, C, B, A };
#else
# error Cannot Detect the endianness of your machine.
# error Consider adding other Endians to this macro if-else
/** TODO: Add PDP endian for fun. */
#endif

  psection(Unpacked Offsets);
  print(A);
  print(B);
  print(C);
  print(D);
  print(E);
  print(F);
  print(G);
  print(H);

  psection(Confirm packed success);
  uint64_t &packed_offset = (uint64_t &)*space;
  print(offset);
  print(packed_offset);
  print((offset == packed_offset));

  psection(Sizes);
  psize(std::uint8_t);
  psize(std::int8_t);
  psize(std::uint16_t);
  psize(std::int16_t);
  psize(std::uint32_t);
  psize(std::int32_t);
  psize(std::uint64_t);
  psize(std::int64_t);

  psection(Limits);
  plimits_ch(std::uint8_t);
  plimits_ch(std::int8_t);
  plimits(std::uint16_t);
  plimits(std::int16_t);
  plimits(std::uint32_t);
  plimits(std::int32_t);
  plimits(std::uint64_t);
  plimits(std::int64_t);
}
