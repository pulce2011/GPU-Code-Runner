#include <cuda_runtime.h>

#include "sum.cuh"

int main() {
    const int n_threads = 1024;
    const int N = 10240;
    const int F = 35;
    float a_h[N], b_h[N], c_h[N], c_h2[N];
    float *a_d, *b_d, *c_d;
    for (int i=0; i<N; i++) {
        a_h[i] = i/35;
        b_h[i] = (i+F)/100;
        c_h2[i] = a_h[i] + b_h[i];
    }
    cudaMalloc(&a_d, sizeof(float)*N);
    cudaMalloc(&b_d, sizeof(float)*N);
    cudaMalloc(&c_d, sizeof(float)*N);
    cudaMemcpy(a_d, a_h, sizeof(float)*N, cudaMemcpyHostToDevice);
    cudaMemcpy(b_d, b_h, sizeof(float)*N, cudaMemcpyHostToDevice);

    sum<<<n_threads, N/n_threads>>>(a_d, b_d, c_d, N);

    cudaMemcpy(c_h, c_d, sizeof(float)*N, cudaMemcpyDeviceToHost);

    for (int i=0; i<N; i++) {
        if (c_h2[i] != c_h[i]) {
            return 1;
        }
    }


    return 0;
}