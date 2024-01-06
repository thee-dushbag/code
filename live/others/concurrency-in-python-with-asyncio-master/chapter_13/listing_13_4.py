import sys

for _ in range(1_000_000):
    # print("Hello World")
    sys.stdout.buffer.write(b"Hello there!!\n")

sys.stdout.flush()
