#include <iostream>
#include <limits.h>
#include <cstdlib>
#include <omp.h>

using namespace std;


int main()
{
    int M = 10, N = 5, K = 6;
	int* A = new int [M * K];
	int* B = new int [K * N];

	int* C = new int [M * N];

	double time_start = omp_get_wtime();
	#pragma omp parallel num_threads(4) shared (A, B, C)
	{
        #pragma omp for schedule(auto)
        for (int i = 0; i < M; ++i)
        {
            for (int j = 0; j < N; ++j)
            {
            C[i*N + j] = 0;
            for (int k = 0; k < K; ++k)
                C[i*N + j] += A[i*K + k] * B[k*N + j];
            }
        }
	}
	double time_end = omp_get_wtime();
	cout << "Time: " << (time_end - time_start) << endl;

	return 0;
}
