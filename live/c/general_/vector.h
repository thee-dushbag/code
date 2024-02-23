#ifndef __VECTOR_H_
#define __VECTOR_H_
#include <stdio.h>

typedef struct {
    int x, y, z;
} vector;

void vector_init(vector *vec, int x, int y, int z) {
    *vec = (vector){ .x = x, .y = y, .z = z };
}

void vector_view(vector const *const vec) {
    printf("<vector(x=%d, y=%d, z=%d)\n", vec->x, vec->y, vec->z);
}

vector vector_addv(vector const *const a, vector const *const b) {
    return { .x = a->x + b->x, .y = a->y + b->y, .z = a->z + b->z };
}

vector vector_adds(vector const *const a, int b) {
    return { .x = a->x + b, .y = a->y + b, .z = a->z + b };
}

vector vector_subv(vector const *const a, vector const *const b) {
    return { .x = a->x - b->x, .y = a->y - b->y, .z = a->z - b->z };
}

vector vector_subs(vector const *const a, int b) {
    return { .x = a->x - b, .y = a->y - b, .z = a->z - b };
}

vector vector_mulv(vector const *const a, vector const *const b) {
    return { .x = a->x * b->x, .y = a->y * b->y, .z = a->z * b->z };
}

vector vector_muls(vector const *const a, int b) {
    return { .x = a->x * b, .y = a->y * b, .z = a->z * b };
}

#endif //__VECTOR_H_
