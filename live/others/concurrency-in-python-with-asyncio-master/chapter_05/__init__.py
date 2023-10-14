import os
import typing as ty

password = os.getenv("PG_PASSWORD") or ""


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
