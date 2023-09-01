#ifndef __SNN_MATH_H_IMPL
#define __SNN_MATH_H_IMPL

#include <stdio.h>

void say_hi(const char *name) {
	printf("Hello %s, how was your day?\n", name);
}

int snn_sum(int x, int y) {
	printf("%d + %d = %d\n", x, y, x + y);
	return x + y;
}

int snn_mul(int x, int y) {
	printf("%d * %d = %d\n", x, y, x * y);
	return x * y;
}

int snn_sub(int x, int y) {
	printf("%d - %d = %d\n", x, y, x - y);
	return x - y;
}

#endif //__SNN_MATH_H_IMPL
