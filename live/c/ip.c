#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <endian.h>

#if BYTE_ORDER == LITTLE_ENDIAN
# define IPADDR(a, b, c, d) { d, c, b, a }
#elif BYTEORDER == BIG_ENDIAN
# define IPADDR(a, b, c, d) { a, b, c, d }
#elif BYTEORDER == PDP_ENDIAN
# define IPADDR(a, b, c, d) { b, a, d, c }
#else
# error "Unsupported BYTE_ORDER."
#endif

union ipv4 {
  uint32_t ipno;
  uint8_t ipch[4];
};

void pip4ch(FILE *stream, union ipv4 *ip) {
  fprintf(
    stream,
    "%d.%d.%d.%d",
# if BYTE_ORDER == LITTLE_ENDIAN
    ip->ipch[3],
    ip->ipch[2],
    ip->ipch[1],
    ip->ipch[0]
# elif BYTE_ORDER == BIG_ENDIAN
    ip->ipch[0],
    ip->ipch[1],
    ip->ipch[2],
    ip->ipch[3]
# elif BYTE_ORDER == PDP_ENDIAN
    ip->ipch[2],
    ip->ipch[3],
    ip->ipch[0],
    ip->ipch[1]
#endif
  );
}
void pip4no(FILE *stream, union ipv4 *ip) {
  fprintf(stream, "%u", ip->ipno);
}

void pip4(FILE *stream, union ipv4 *ip) {
  fprintf(stream, "ipv4(");
  pip4ch(stream, ip);
  fprintf(stream, ", ");
  pip4no(stream, ip);
  fputc(')', stream);
}

void allips(uint32_t start, uint32_t end) {
  union ipv4 ip;
  while ( start <= end ) {
    ip.ipno = start;
    pip4ch(stdout, &ip);
    fputc('\t', stdout);
    pip4no(stdout, &ip);
    fputc('\n', stdout);
    start++;
  }
}

int main() {
  // allips(0, UINT_MAX);
  union ipv4 ips[5] = {
    {.ipch=IPADDR(192,168,0,100)},
    {.ipch=IPADDR(192,168,0,101)},
    {.ipch=IPADDR(192,168,1,3)},
    {.ipch=IPADDR(10,74,3,133)},
    {.ipch=IPADDR(174,34,99,126)},
  };

  for (int i = 0; i < 5; i++) {
    pip4(stdout, ips + i);
    fputc('\n', stdout);
  }
}

