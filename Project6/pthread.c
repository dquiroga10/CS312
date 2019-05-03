/*
Danny Quiroga 
April 16, 2019
CSCI 312
Pthread.c creates a producer that pushes tasks while two consumer threads
and pop tasks from the task queue, which can hold a maximum of 2 tasks.
*/

#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>


// declarations of global variables
pthread_mutex_t task_queue_lock;
int task_available;
int n;
void *consumer_thread_data1 (void *);
void *consumer_thread_data2 (void *);
int task_queue[2] = {-1, -1};
int tasks_complete[2] = {0, 0};

//producer function
void *producer(){
 //while task_av is less than n
	while (task_available < n){
		pthread_mutex_lock(&task_queue_lock); //locks queue
		int inserted = 0; //initilize with 0 tasks inserted
   // while there is space in the task queue and inserted value is less than 2 since we can not insert more than 
		// two things in our queue

		 while ((task_queue[0] != 1 || task_queue[1] != 1) && inserted < 2){
      // if first spot in taskqueue is empty and inserted + available tasks are less than n
      //then producer inserts 1 task
		    if ((task_queue[0] == 0 || task_queue[0] == -1)&& (inserted + task_available) < n){
		    	task_queue[0] = 1;
		    	printf("Producer inserted %i \n", 1);
		    	inserted++;
		    }
      //if second spot in queue is empty, and tasks are less than n
      //then producer inserts 1 task
		    if ((task_queue[1] == 0 || task_queue[1] == -1) && (inserted + task_available) < n){
		    	task_queue[1] = 1;
		    	printf("Producer inserted %i \n", 1);
		    	inserted++;
		    }
      //if tasks are greater or equal to n, exit
		    if((inserted + task_available) >= n){
		    	break;
		    }
		 }
   //add available tasks to inserted, unlock queue
		 task_available += inserted;
		 pthread_mutex_unlock(&task_queue_lock);
	}
 //exit pthread
	pthread_exit(0);
}


//consumer function with thread_data as parameter
void *consumer1(void *consumer_thread_data1){

 // when tasks available are less than n
	while (task_available < n){
  //declarations and lock queue
		pthread_mutex_lock(&task_queue_lock);
		int extracted, *num_extract, temp;
		num_extract = (int *) consumer_thread_data1;

		extracted = 0;
		// this if statement just checks to make sure that there is a task in the queue or else
		// it is pointless to extract a task from an empty queue
		if (task_queue[0] == 1 || task_queue[1] == 1){
		if(task_queue[0] == 1){
			temp = 1;
			task_queue[0] = 0;
			extracted++;
		}
		// this if statement checks to make that if there is a task in the other position and
		// also to make sure that a task has not been extracted already by this task this time 
		// around since the consumers can only extract one task at a time
		else if (task_queue[1] == 1 && extracted == 0){
			temp = 1;
			task_queue[1] = 0;
			extracted++;
		}
  //prints which consumer extracted the task
		printf("Consumer 1 extracted %i \n",temp);
		}

		*num_extract += extracted;
		pthread_mutex_unlock(&task_queue_lock);
	}
	pthread_exit(0);
}

void *consumer2(void *consumer_thread_data2){

 // when tasks available are less than n
	while (task_available < n){
  //declarations and lock queue
		pthread_mutex_lock(&task_queue_lock);
		int extracted, *num_extract, temp;
		num_extract = (int *) consumer_thread_data2;

		extracted = 0;
		// this if statement just checks to make sure that there is a task in the queue or else
		// it is pointless to extract a task from an empty queue
		if (task_queue[0] == 1 || task_queue[1] == 1){
		if(task_queue[0] == 1){
			temp = 1;
			task_queue[0] = 0;
			extracted++;
		}
		// this if statement checks to make that if there is a task in the other position and
		// also to make sure that a task has not been extracted already by this task this time 
		// around since the consumers can only extract one task at a time
		else if (task_queue[1] == 1 && extracted == 0){
			temp = 1;
			task_queue[1] = 0;
			extracted++;
		}
  //prints which consumer extracted the task
		printf("Consumer 2 extracted %i \n",temp);
		}

		*num_extract += extracted;
		pthread_mutex_unlock(&task_queue_lock);
	}
	pthread_exit(0);
}


// main function:
int main(int argc, char **argv){

	if(argc != 2){
		printf("Expected 2 parameters, filename integer\n");
		return 0;
	}
	pthread_t prod, con1, con2;
	pthread_attr_t atrib;
	pthread_attr_init(&atrib);
	pthread_mutex_init(&task_queue_lock, NULL);

	//declares N tasks, converts to an int
	n = atoi(argv[1]);

	//creates producer and 2 consumer threads, there is two different consumer functions because we need different print statements based off
	//which consumer is extracting, I could have simplified this by using a struct to maintain two sets of info the data struct and string
	pthread_create(&prod, &atrib, producer, NULL);
	pthread_create(&con1, &atrib, consumer1, (void *) &tasks_complete[0]);
	pthread_create(&con2, &atrib, consumer2, (void *) &tasks_complete[1]);

	//starts with 0 tasks available and mutex on the task queue
	task_available = 0;

 // joins threads
	pthread_join(prod, NULL);
	pthread_join(con1, NULL);
	pthread_join(con2, NULL);

//Print Statements to show how many tasks each consumer extracted
	printf("Consumer 1 extracted %i number of tasks \n", tasks_complete[0]);
	printf("Consumer 2 extracted %i number of tasks \n", tasks_complete[1]);
	pthread_exit(0);
	return 0;
}
