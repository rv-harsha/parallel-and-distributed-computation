#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char** argv) {
    int size, rank;
    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    int message;
    
    if (rank == 0) {
        message = 451;
        printf("Process 0: Initially message = %d\n", message);
        MPI_Send(&message, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
        MPI_Recv(&message, 1, MPI_INT, 3, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Process 0: Received message = %d. Done!\n", message);
    }
    else if(rank == 1){
        MPI_Recv(&message, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        message++;
        printf("Process 1: message = %d\n", message);
        MPI_Send(&message, 1, MPI_INT, 2, 0, MPI_COMM_WORLD);
    }
    else if(rank == 2){
        MPI_Recv(&message, 1, MPI_INT, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        message++;
        printf("Process 2: message = %d\n", message);
        MPI_Send(&message, 1, MPI_INT, 3, 0, MPI_COMM_WORLD);
    }
    else if(rank == 3){
        MPI_Recv(&message, 1, MPI_INT, 2, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        message++;
        printf("Process 3: message = %d\n", message);
        MPI_Send(&message, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}