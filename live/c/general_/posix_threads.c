#include <pthread.h>
#include <stdio.h>
#include <assert.h>
#include <unistd.h>

typedef struct CountParam {
    int start, stop, step;
} CountParam_t;

void init_count_param(CountParam_t* count_param, int start, int stop, int step) {
    count_param->start = start;
    count_param->stop = stop;
    count_param->step = step;
}

void count(int start, int stop, int step) {
    assert(start < stop);
    for(int i = start; i < stop; i += step) {
        printf("Count[%d, %d, %d] at: %d\n", start, stop, step, i);
        sleep(1);
    }
}

void *count_thread_task(void *count_param) {
    CountParam_t* cp = (CountParam_t*)count_param;
    count(cp->start, cp->stop, cp->step);
    return NULL;
}

int main(int argc, char **argv) {
    pthread_t counter_one, counter_two, counter_three;
    CountParam_t param_one, param_two, param_three;
    init_count_param(&param_one, 11, 21, 1);
    init_count_param(&param_two, 11, 21, 1);
    init_count_param(&param_three, 11, 21, 1);
    pthread_create(&counter_one, NULL, count_thread_task, &param_one);
    pthread_create(&counter_two, NULL, count_thread_task, &param_two);
    pthread_create(&counter_three, NULL, count_thread_task, &param_three);
    pthread_join(counter_one, NULL);
    pthread_join(counter_two, NULL);
    pthread_join(counter_three, NULL);
}