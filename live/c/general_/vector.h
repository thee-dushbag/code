#ifndef __VECTOR_H_
#define __VECTOR_H_
#include <stdio.h>

typedef struct {
    int x, y, z;
} vector;

void vector_init(vector *vec, int x, int y, int z) {
    vec->x = x;
    vec->y = y;
    vec->z = z;
}

void vector_view(vector const *const vec) {
    printf("<vector(x=%d, y=%d, z=%d)\n", vec->x, vec->y, vec->z);
}

vector vector_addv(vector const *const a, vector const *const b) {
    vector res;
    res.x = a->x + b->x;
    res.y = a->y + b->y;
    res.z = a->z + b->z;
    return res;
}

vector vector_adds(vector const *const a, int b) {
    vector res;
    res.x = a->x + b;
    res.y = a->y + b;
    res.z = a->z + b;
    return res;
}

vector vector_subv(vector const *const a, vector const *const b) {
    vector res;
    res.x = a->x - b->x;
    res.y = a->y - b->y;
    res.z = a->z - b->z;
    return res;
}

vector vector_subs(vector const *const a, int b) {
    vector res;
    res.x = a->x - b;
    res.y = a->y - b;
    res.z = a->z - b;
    return res;
}

vector vector_mulv(vector const *const a, vector const *const b) {
    vector res;
    res.x = a->x * b->x;
    res.y = a->y * b->y;
    res.z = a->z * b->z;
    return res;
}

vector vector_muls(vector const *const a, int b) {
    vector res;
    res.x = a->x * b;
    res.y = a->y * b;
    res.z = a->z * b;
    return res;
}

#endif //__VECTOR_H_
