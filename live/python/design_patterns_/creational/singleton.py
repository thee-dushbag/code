"""Implementing singleton design pattern in python.
Singleton -> Not Thread Safe
SingletonThreadSafe -> Thread Safe"""

__all__ = ["Singleton", "SingletonThreadSafe"]

import threading as th


class Singleton(type):
    _instances: dict = {}

    def __call__(self, *args, **kwargs) -> "Singleton":
        if not self in Singleton._instances:
            Singleton._instances[self] = super().__call__(*args, **kwargs)
        return Singleton._instances[self]


class SingletonThreadSafe(type):
    _instances: dict = {}
    _lock: th.Lock = th.Lock()

    def __call__(self, *args, **kwargs) -> "Singleton":
        SingletonThreadSafe._lock.acquire()
        if not self in Singleton._instances:
            Singleton._instances[self] = super().__call__(*args, **kwargs)
        SingletonThreadSafe._lock.release()
        return Singleton._instances[self]
