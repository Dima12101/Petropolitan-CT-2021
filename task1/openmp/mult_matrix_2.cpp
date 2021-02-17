#include <iostream>
#include <limits.h>
#include <cstdlib>
#include <omp.h>

using namespace std;

int** generate_matrix(int number_row, int number_col)
{
	int** matrix = new int* [number_row];
	for (size_t i = 0; i < number_row; i++)
	{
		matrix[i] = new int[number_col];
	}
	return matrix;
}

int** generate_matrix_rnd(int number_row, int number_col)
{
	int** matrix = new int* [number_row];
	for (size_t i = 0; i < number_row; i++)
	{
		matrix[i] = new int[number_col];
		for (size_t j = 0; j < number_col; j++)
		{
			matrix[i][j] = rand() % 100;
		}
	}
	return matrix;
}


int main()
{
    int M = 10, N = 5, K = 6;
	int** A = generate_matrix_rnd(M, K);
	int** B = generate_matrix_rnd(K, N);

	int** C = generate_matrix(M, N);

	double time_start = omp_get_wtime();
	#pragma omp parallel num_threads(4) shared (A, B, C)
	{
        #pragma omp for schedule(auto)
        for (int i = 0; i < M; ++i)
        {
            for (int j = 0; j < N; ++j)
            {
            C[i][j] = 0;
            for (int k = 0; k < K; ++k)
                C[i][j] += A[i][k] * B[k][j];
            }
        }
	}
	double time_end = omp_get_wtime();
	cout << "Time: " << (time_end - time_start) << endl;

	return 0;
}
