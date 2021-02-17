#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 16

__global__ void matrixMult(const double *A, const double *B, double *C, int K, int N)
{
    int i0 = blockDim.y * blockIdx.y + threadIdx.y;
    int j0 = blockDim.x * blockIdx.x + threadIdx.x;
    
    double sum = 0;
    for (int k = 0; k < K; k++)
        sum += A[i0 * K + k] * B[k * N + j0];
    C[N * i0 + j0] = sum;
}

void init_matrix_rnd(double* &matrix, int number_row, int number_col)
{
	for (size_t i = 0; i < number_row * number_col; i++)
		matrix[i] = double(rand()) / double(1000);
}

int main()
{
    //start, stop - for Kernel time
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    // количество строк и столбцов матриц A[MxK] и B[KxN]
    int M = 32, K = 48, N = 32;
    // Размеры матриц A и B должны нацело делиться на размер блока.

    size_t Asize = M * K * sizeof(double);
    size_t Bsize = K * N * sizeof(double);
    size_t Csize = M * N * sizeof(double);

    double *h_A = (double *)malloc(Asize);
    double *h_B = (double *)malloc(Bsize);
    double *h_C = (double *)malloc(Csize);

    init_matrix_rnd(h_A, M, K);
    init_matrix_rnd(h_B, K, N);

    double *d_A = NULL;
    cudaMalloc((void **)&d_A, Asize);

    double *d_B = NULL;
    cudaMalloc((void **)&d_B, Bsize);

    double * d_C = NULL;
    cudaMalloc((void **)&d_C, Csize);
    cudaMemcpy(d_A, h_A, Asize, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, Bsize, cudaMemcpyHostToDevice);

    dim3 threadsPerBlock = dim3(BLOCK_SIZE, BLOCK_SIZE);
    dim3 blocksPerGrid = dim3(N / BLOCK_SIZE, M / BLOCK_SIZE);

    cudaEventRecord(start, 0);

    matrixMult<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, K, N);

    cudaEventRecord( stop, 0);
    cudaEventSynchronize( stop );
    float KernelTime;
    cudaEventElapsedTime( &KernelTime, start, stop);
    printf("KernelTime: %.2f milliseconds\n", KernelTime);

    cudaMemcpy(h_C, d_C, Csize, cudaMemcpyDeviceToHost);

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(h_A);
    free(h_B);
    free(h_C);
    cudaEventDestroy( start );
    cudaEventDestroy( stop );

    return 0;
}