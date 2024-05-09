def numbers(name: str, start: int, stop: int):
    assert start <= stop
    while start < stop:
        print(f"{name}[{stop}]: computed={start}")
        yield start
        start += 1
    print(f"{name}: finished={stop}")


from itertools import tee

I, J = tee(numbers("hey", 10, 16))

print("Yield I")
for i in I:
    print(f"I::consumed={i}")
print("Yield J")
for j in J:
    print(f"J::consumed={j}")
