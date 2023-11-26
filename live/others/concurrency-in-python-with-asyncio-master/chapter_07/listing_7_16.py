import hashlib
import os
import random
import string
import time

ascii_lowercase = string.ascii_lowercase.encode()

def random_password(length: int) -> bytes:
    elements = random.choices(ascii_lowercase, k=length)
    return b"".join(bytes(e) for e in elements)


passwords = (random_password(10) for _ in range(10000))


def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


start = time.time()

for password in passwords:
    hash(password)

end = time.time()
print(end - start)
