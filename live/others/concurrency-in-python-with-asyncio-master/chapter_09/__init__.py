"""
In this chapter you learn about web applications
from aiohttp, flask to django applications.
"""

import os
import typing as ty

password = os.getenv("PG_PASSWORD", "")


class Credential(ty.TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str


cred = Credential(
    host="localhost",
    port=5432,
    user="simon",
    password=password,
    database="learnasyncio",
)