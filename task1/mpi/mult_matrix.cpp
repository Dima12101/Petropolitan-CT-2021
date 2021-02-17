#include<mpi.h>
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<iostream>

using namespace std;

int ProcNum; 
int ProcRank;

//***********************************************************
void PrintMatrix(double* pMatrix,int Size) {
    for (int i = 0; i < Size; i++) {
        printf("\n");
        for (int j=0; j < Size; j++)
            printf("%7.4f ", pMatrix[i * Size + j]);
    }
}

//-------------------------------------------------
double* generate_matrix_rnd(int number_row, int number_col)
{
    double* matrix = new double [number_row * number_col];
	for (size_t i = 0; i < number_row * number_col; i++)
		matrix[i] = double(rand()) / double(1000);
	return matrix;
}

//-------------------------------------------------
void InitProcess(double* &A, double* &B, double* &C , int &Size) {
    MPI_Comm_size(MPI_COMM_WORLD, &ProcNum);
    MPI_Comm_rank(MPI_COMM_WORLD, &ProcRank);

    if (ProcRank == 0) {
        cout << "ProcNum: " << ProcNum << endl;
        A = generate_matrix_rnd(Size, Size);
        B = generate_matrix_rnd(Size, Size);

        C = new double [Size * Size];
    }
}

//-------------------------------------------------
void Flip(double *&B, int Size) {
    double temp = 0.0;
    for (int i = 0; i < Size; i++){
        for (int j = i + 1; j < Size; j++){
            temp = B[i * Size + j];
            B[i * Size + j] = B[j * Size + i];
            B[j * Size + i] = temp;
        }
    }
}

//-------------------------------------------------
void MatrixMultiplicationMPI(double *&A, double *&B, double *&C, int &Size) {
    int i, j, k, p, ind;
    double temp;
    MPI_Status Status;
    
    int ProcPartSize = Size / ProcNum; // Т.е. сколько строк/столбов отводится процессу
    int ProcPartElem = ProcPartSize * Size;
    
    double* bufA = new double[ProcPartElem];
    double* bufB = new double[ProcPartElem];
    double* bufC = new double[ProcPartElem];
    
    if (ProcRank == 0)
        Flip(B,Size);
 
    MPI_Scatter(A, ProcPartElem, MPI_DOUBLE, bufA, ProcPartElem, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Scatter(B, ProcPartElem, MPI_DOUBLE, bufB, ProcPartElem, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    temp=0.0;
    for(i = 0; i < ProcPartSize; i++){
        for(j = 0; j < ProcPartSize; j++){
            for(k = 0; k < Size; k++) 
                temp += bufA[i * Size + k] * bufB[j * Size + k];
            bufC[i * Size + j + ProcPartSize * ProcRank] = temp;
            temp = 0.0;
        }
    }

    int NextProc; int PrevProc;
    for(p = 1; p < ProcNum; p++) {
        
        NextProc = ProcRank + 1;
        if (ProcRank == ProcNum - 1) NextProc = 0;
        
        PrevProc = ProcRank - 1;
        if (ProcRank == 0) PrevProc = ProcNum - 1;
        
        MPI_Sendrecv_replace(bufB, ProcPartSize, MPI_DOUBLE, NextProc, 0, PrevProc, 0, MPI_COMM_WORLD, &Status);
        
        temp=0.0;
        for (i = 0; i < ProcPartSize; i++) {
            for(j = 0; j < ProcPartSize; j++) {
                for(k = 0; k < Size; k++){
                    temp += bufA[i * Size + k] * bufB[j * Size + k];
                }
                if (ProcRank - p >= 0 )
                    ind = ProcRank - p;
                else 
                    ind = ProcNum - p + ProcRank;
                bufC[i * Size + j + ProcPartSize * ind] = temp;
                temp=0.0;
            }
        }
    }
    MPI_Gather(bufC, ProcPartElem, MPI_DOUBLE, C, ProcPartElem, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    delete []bufA;
    delete []bufB;
    delete []bufC;
}

//--------------------------------------------------------

int main(int argc, char* argv[]) {
    MPI_Init ( &argc, &argv );  
    
    double *A, *B, *C;
    int Size = 24;
    /*
    Размер матрицы должен быть не меньше кол-ва процессов.
    Размер матрицы должен нацело делиться на кол-во процессов.
    */
    InitProcess(A, B, C, Size);

    double time_start = MPI_Wtime();
    MatrixMultiplicationMPI(A, B, C, Size);
    double time_end = MPI_Wtime();
    if (ProcRank == 0)
        cout << "Time: " << (time_end - time_start) << endl;
    
    MPI_Finalize();

    return 0;
}