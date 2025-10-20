#include <cuda_runtime.h>
#include <stdio.h>

__global__ void sum(float *a, float *b, float *c, int N)
{
    int id = blockIdx.x * blockDim.x + threadIdx.x;

    if(id >= N)
        return;

    c[id] = a[id] + b[id];

    printf("c[%d] = %f\n", id, c[id]);
}