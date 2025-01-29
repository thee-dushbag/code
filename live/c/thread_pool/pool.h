#pragma once

#include <threads.h>

#ifndef MAX_QNODE_PACK
#define MAX_QNODE_PACK 20
#endif

typedef struct packaged_task_t {
  void *arg;
  void (*function)(void *);
} task_t;

struct node_t {
  task_t tasks[MAX_QNODE_PACK];
  struct node_t *next;
};

struct queue_t {
  unsigned tidx, hidx;
  struct node_t *head, *tail;
};

struct pool_t {
  long workers : 19, shutting_down : 1, tasks : 44;
  mtx_t mtx;
  cnd_t cnd;
  thrd_t *worker_ids;
  struct queue_t taskq;
};

/* Enqueue (copied) *task for execution. */
int pool_push(struct pool_t *pool, task_t *task);
/* Initialize the Pool for use. */
void pool_init(struct pool_t *pool, unsigned worker_cnt);
/* Wait until the task_queue is empty. */
void pool_wait(struct pool_t *pool);
/* Destroy the pool with all pending tasks. */
void pool_destroy(struct pool_t *pool);
/* Wait all pending tasks to be executed and destroy the pool. */
void pool_destroy_wait(struct pool_t *pool);

