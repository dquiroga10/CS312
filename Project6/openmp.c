/*
Danny Quiroga
April 24, 2019
Openmp.c creates n threads that use a random number generator to use as samples. The samples are summed with openMP reduction and compute accurate pi estimations.
*/

#include <stdlib.h>
#include <omp.h>
#include <stdio.h>

//global variables
//if thread number is not specified by compile line, then 4 threads will be used
//hits and total_hits are used to keep track of which thread is doing what
int num_threads = 4;
int hits[0];
int total_hits = 0;

//compute_pi() generates samples for threads
int compute_pi(){
	int i;
	double x_cord, y_cord;
	int local_hits;
	int sample_points_per_thread;
    
	sample_points_per_thread = 975500 + rand()%50000; //uses random function for random samples
	total_hits += sample_points_per_thread;
	local_hits = 0;
    //for loop gathers random values for x and y coordinates in a circle
	for(i = 0; i < sample_points_per_thread; i++){
		x_cord = (double)(rand()) / (RAND_MAX) - 0.5;
		y_cord = (double)(rand()) / (RAND_MAX) - 0.5;
        //increment local hits if x^2 + y^2 is less than .25
		if ((x_cord * x_cord + y_cord * y_cord) < 0.25){
			local_hits++;
		}
	}
	return local_hits;
}

//main() uses openMP to compute pi from samples
int main(int argc, char **argv){
	int i;
	float sum;
    
    //casts number inputted from compile as an int, and saves it as num_threads
	if(argv[1] != NULL){
		num_threads = atoi(argv[1]);
	}
	hits[num_threads];
    //parallel region direction: create n threads, where n can be inputted from compile line
    //else it will create 4 threads
	#pragma omp parallel num_threads(num_threads)
 {
    //for directive
	#pragma omp for
    //for each thread, compute pi
	for (i = 0; i < num_threads; i++) {
		hits[i] = compute_pi();
	   }
 }
    //reduction clause computes local sum as a float in each thread
	#pragma omp parallel reduction(+: sum) num_threads(num_threads)
 {
		#pragma omp for
		for (i = 0; i < num_threads; i++) {
			sum = (float) hits[i];
		 }
 }
    //computes pi as a float with the sum of all the local sums divided by total hits times four
	float pi = (sum / (float)total_hits) * 4.0;
	printf("Pi = %f \n", pi);
}
