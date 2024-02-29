import numpy as np

m = np.matrix([1, 2, 3, 4, 5, 6])
m = m.reshape((2, 3))
print(m)

s = 3 * m
print(s)
m2 = np.arange(7, 13).reshape(2, 3)
print(m2)
print(m2 + m)
print(m2 * m.transpose())
print(m.transpose() * m2)  # Non-commutative
print(m.trace()[0, 0])
