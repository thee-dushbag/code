from threading import Lock as Lock, Thread
from typing import List

list_lock = Lock()


def sum_list(int_list: List[int]) -> int:
    print("Waiting to acquire lock...")
    with list_lock:
        print("Acquired lock.")
        if int_list:
            print("Summing rest of list.")
            head, *tail = int_list
            return head + sum_list(tail)
        print("Finished summing.")
        return 0


thread = Thread(target=sum_list, args=([1, 2, 3, 4],))
thread.start()
thread.join()
