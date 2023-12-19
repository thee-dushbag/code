"""
In this chapter you learn about the basics or
microservices using aiohttp, flask and django.
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