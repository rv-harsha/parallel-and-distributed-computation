#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <pthread.h>

#define NUM_THREADS 2

pthread_mutex_t mutex;
pthread_cond_t cv;

struct  thread_data{
    int     thread_id;
    int     *var_ptr;
};

struct  thread_data  thread_data_array[NUM_THREADS];

void *increase_var(void *threadarg){
    struct  thread_data * my_data;
    my_data = (struct thread_data *) threadarg;
    int my_id = my_data->thread_id;
    int *var_ptr = my_data->var_ptr;

    // increase var 5 times
    for (int i=0; i<5; i++) {
    	pthread_mutex_lock(&mutex);
    	// thread 0 increases var when var is even; thread 1 increases var when var is odd
        while (*var_ptr % 2 != my_id) {
            pthread_cond_wait(&cv, &mutex);
        }
		(*var_ptr)++;
		printf("Thread %d increased var to %d\n", my_id, *var_ptr);
		pthread_cond_signal(&cv);
    	pthread_mutex_unlock(&mutex);
    }
    pthread_exit(NULL);
}


int main(void){
	int i, rc;
	pthread_t  threads[NUM_THREADS];
	int var = 0;

	pthread_mutex_init(&mutex, NULL);
	pthread_cond_init(&cv, NULL);
	
	for(i=0; i<NUM_THREADS; i++) {
        thread_data_array[i].thread_id = i;
        thread_data_array[i].var_ptr = &var;
        rc = pthread_create(&threads[i], NULL, increase_var, (void *) &thread_data_array[i] );
        if (rc) { printf("ERROR; return code from pthread_create() is %d\n", rc); exit(-1);}
    }
    for(i=0; i<NUM_THREADS; i++) {
        rc = pthread_join(threads[i], NULL);
        if (rc) { printf("ERROR; return code from pthread_join() is %d\n", rc); exit(-1);}
    }
    printf("Final var value is %d\n", var);
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cv);
	
	return 0;
}