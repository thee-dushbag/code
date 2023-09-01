#ifndef __MAKE_C_H_MATH_IMPL_
#define __MAKE_C_H_MATH_IMPL_

#include <stdio.h>

int add(int x, int y) {
    int c = x + y;
    printf("%d + %d = %d\n", x, y, c);
    return c;
}

int sub(int x, int y) {
    int c = x - y;
    printf("%d - %d = %d\n", x, y, c);
    return c;
}

int mul(int x, int y) {
    int c = x * y;
    printf("%d * %d = %d\n", x, y, c);
    return c;
}

#endif //__MAKE_C_H_MATH_IMPL_