#include <stdlib.h>
#include <stdio.h>
#include <cublas.h>
#include <time.h>

#define HEIGHT 1024
#define WIDTH 1024
#define BLOCK_SIZE 32


__global__ void matrix_mult(int *a, int *b, int *c){
	int threadRow = threadIdx.y;
	int threadCol = threadIdx.x;

	int row = blockIdx.y * blockDim.y + threadIdx.y;
	int col = /*your code here*/;

	int c_val = 0;
	for (int i = 0; i<(WIDTH/BLOCK_SIZE); i++) {
		__shared__ int a_share[BLOCK_SIZE][BLOCK_SIZE];
		/*your code here to declare b_share*/

		// each thread reads one element from both A and B matrices into the shared sub-matrices
		a_share[threadRow][threadCol] = a[/*your code here*/];
		b_share[threadRow][threadCol] = b[/*your code here*/];

		// make sure the sub-matrices are loaded before starting the computation
		__syncthreads();

		for (int i=0; i<BLOCK_SIZE; i++) {
			c_val += a_share[/*your code here*/][i] * b_share[i][/*your code here*/];
		}

		// make sure every thread is done computing before loading new sub-matrices
		__syncthreads();

	}

	c[row * WIDTH + col] = c_val;
}

int main(){
  int i;
  int *a = (int*)malloc(sizeof(int) * HEIGHT * WIDTH);
	int *b = (int*)malloc(sizeof(int) * HEIGHT * WIDTH);
  int *c = (int*)malloc(sizeof(int) * HEIGHT * WIDTH);
	for(i=0; i<WIDTH * HEIGHT; i++){
		a[i]=1;
		b[i]=2;
  	}

	int *gpu_a, *gpu_b, *gpu_c;
	/*your code here to malloc gpu_a, gpu_b, gpu_c on device*/

	struct timespec start, stop;
	double time;

	/*your code here to copy a and b from host to device*/

	/*your code here to create dimGrid and dimBlock*/

	if( clock_gettime( CLOCK_REALTIME, &start) == -1 ) { perror( "clock gettime" );}

	matrix_mult<<<dimGrid, dimBlock>>>(gpu_a, gpu_b, gpu_c);
	/*your code here to copy gpu_c from device to host*/

	if( clock_gettime( CLOCK_REALTIME, &stop) == -1 ) { perror( "clock gettime" );}
	time = (stop.tv_sec - start.tv_sec)+ (double)(stop.tv_nsec - start.tv_nsec)/1e9;
	printf("time is %f ns\n", time*1e9);

	printf("c[451][451]=%d\n", c[451*1024+451]);

	free(a);
	free(b);
	free(c);
	/*your code here to free device memory*/
	return 0;
}
