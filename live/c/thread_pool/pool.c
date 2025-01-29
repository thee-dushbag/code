#include "pool.h"
#include <assert.h>
#include <stdlib.h>
#include <threads.h>

static struct node_t *node_alloc(struct node_t *head) {
  struct node_t *node_ptr = (struct node_t *)malloc(sizeof(struct node_t));
  node_ptr->next = NULL;
  if (head)
    head->next = node_ptr;
  return node_ptr;
}

static struct node_t *node_free(struct node_t *tail) {
  struct node_t *next = tail->next;
  free(tail);
  return next;
}

static void queue_init(struct queue_t *queue) {
  queue->head = queue->tail = node_alloc(NULL);
  queue->tidx = queue->hidx = 0;
}

static void queue_destroy(struct queue_t *queue) {
  struct node_t *head = queue->tail;
  while (head != NULL) {
    head = node_free(head);
  }
}

static void queue_push(struct queue_t *queue, task_t *task) {
  queue->head->tasks[queue->hidx] = *task;
  queue->hidx++;
  if (queue->hidx == MAX_QNODE_PACK) {
    queue->head = node_alloc(queue->head);
    queue->hidx = 0;
  }
}

static int queue_empty(struct queue_t *queue) {
  return queue->head == queue->tail && queue->hidx == queue->tidx;
}

static task_t queue_pop(struct queue_t *queue) {
  task_t task = queue->tail->tasks[queue->tidx];
  queue->tidx++;
  if (queue->tidx == MAX_QNODE_PACK) {
    queue->tail = node_free(queue->tail);
    queue->tidx = 0;
  }
  return task;
}

static int pool__pop(struct pool_t *pool, task_t *task) {
  if (pool->shutting_down)
    return 0;
  mtx_lock(&pool->mtx);
  while (pool->tasks == 0 && !pool->shutting_down) {
    cnd_wait(&pool->cnd, &pool->mtx);
  }
  int status = 0;
  if (pool->tasks && !pool->shutting_down) {
    *task = queue_pop(&pool->taskq);
    pool->tasks--;
    status = 1;
  }
  mtx_unlock(&pool->mtx);
  return status;
}

int pool_push(struct pool_t *pool, task_t *task) {
  if (pool->shutting_down)
    return 0;
  mtx_lock(&pool->mtx);
  queue_push(&pool->taskq, task);
  pool->tasks++;
  cnd_signal(&pool->cnd);
  mtx_unlock(&pool->mtx);
  return 1;
}

static int pool__worker_mainloop(void *arg) {
  struct pool_t *pool = (struct pool_t *)arg;
  task_t task;
  while (pool__pop(pool, &task))
    task.function(task.arg);
  return thrd_success;
}

void pool_init(struct pool_t *pool, unsigned worker_cnt) {
  pool->tasks = 0;
  pool->shutting_down = 0;
  pool->workers = worker_cnt;
  mtx_init(&pool->mtx, mtx_plain);
  cnd_init(&pool->cnd);
  queue_init(&pool->taskq);
  thrd_t *workers = (thrd_t *)calloc(worker_cnt, sizeof(thrd_t));
  for (size_t i = 0; i < worker_cnt; i++)
    thrd_create(workers + i, pool__worker_mainloop, pool);
  pool->worker_ids = workers;
}

static void pool__noop(void *arg) { *(int *)arg = 1; }

void pool_wait(struct pool_t *pool) {
  int marker = 0;
  task_t noop = {.arg = &marker, .function = pool__noop};
  pool_push(pool, &noop);
  while (marker == 0)
    thrd_yield();
}

void pool_destroy(struct pool_t *pool) {
  mtx_lock(&pool->mtx);
  pool->shutting_down |= 1;
  cnd_broadcast(&pool->cnd);
  mtx_unlock(&pool->mtx);
  for (unsigned i = 0; i < pool->workers; i++)
    thrd_join(pool->worker_ids[i], NULL);
  mtx_destroy(&pool->mtx);
  cnd_destroy(&pool->cnd);
  queue_destroy(&pool->taskq);
}

void pool_destroy_wait(struct pool_t *pool) {
  pool_wait(pool);
  pool_destroy(pool);
}

