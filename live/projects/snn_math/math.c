#include <stdio.h>
#include <snn_math_dec.h>

struct xy_vals
{
    int x, y;
};

void bundle(struct xy_vals *vals)
{
    snn_sum(vals->x, vals->y);
    snn_sub(vals->x, vals->y);
    snn_mul(vals->x, vals->y);
}

int main()
{
    // int vals[8][2] = {{1, 2}, {3, 4}, {5, 6}, {7, 8}, {9, 10}, {11, 12}, {13, 14}, {15, 16}};
    int vals[8][2] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
    struct xy_vals values[8];
    for (int i = 0; i < 8; i++)
    {
        values[i].x = vals[i][0];
        values[i].y = vals[i][1];
    }

    for (int i = 0; i < 8; i++)
        bundle(values + i);
}