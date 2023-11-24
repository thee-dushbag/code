import time
from threading import Lock, Thread

lock_a = Lock()
lock_b = Lock()


def a():
    with lock_a:  # A
        print("Acquired lock a from method a!")
        time.sleep(1)  # B
        with lock_b:  # C
            print("Acquired both locks from method a!")


def b():
    with lock_b:  # D
        print("Acquired lock b from method b!")
        with lock_a:  # E
            print("Acquired both locks from method b!")


thread_1 = Thread(target=a)
thread_2 = Thread(target=b)
thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()

# This code introduces a deadlock.
# Ways to avoid dead locks.
# 1. Use one lock if necessary.
# 2. Refactor code, ie, changing
#    the sequence of lock aquirement
#    can prevent the deadlock. eq, acquiring
#    lock_a then lock_b in both methods a and b
#    would prevent the deadlock or better yet, using
#    one lock in this application would also
#    prevent the deadlock entirely.
# 3. Some deadlocks are quite rare to occur as by
#    by definition, deadlocks occur when a specific
#    chain of events take place, like in this example,
#    if the deadlock is extremely rare, the it isn't worth
#    fixing, that is if the fix would result in more work
#    as compared to simply restarting the application.