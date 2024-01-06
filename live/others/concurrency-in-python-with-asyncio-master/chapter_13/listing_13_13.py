import time, random

while name := input("Name: "):
    for _ in range(random.randrange(1, 11)):
        time.sleep(0.5)
        print(f"  Hello {name}, how was your day?")
