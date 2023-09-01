#include <stdio.h>
#include <snn_math_dec.h>

int main() {
    const char *name = "Simon Nganga Njoroge";
    say_hi(name);
    int x = 100, y = 20, r;
    r = snn_sum(x, y);
    r = snn_mul(x, y);
    r = snn_sub(x, y);
}