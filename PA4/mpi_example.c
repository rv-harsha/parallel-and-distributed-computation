#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char const *argv[])
{
	int npes, myrank;

	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &npes);  // total number of processes
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	printf("From process %d out of %d, Hello World!\n",myrank, npes);

	int msg = 451;
	MPI_Status status;
	if (myrank == 0) {
		// send to 1
	} else if (myrank == 1) {
		// recv from 1
		// send to 2
	} else if (myrank == 2) {
		// recv from 2
		// send to 3
	} else if (myrank == 3) {
		// recv from 3
		// print msg
	}
	MPI_Finalize();
	return 0;
}