# Longest Common Substring.


def create_matrix(width: int, height: int, init=0):
    return [[init for _ in range(width)] for _ in range(height)]


def longest_common_substring(s1: str, s2: str, /):
    substring_size, point = 0, 0
    width, height = len(s2), len(s1)
    grid = create_matrix(width, height)

    for i2, c2 in enumerate(s2):
        for i1, c1 in enumerate(s1):
            top_left = 0
            if i2 and i1:
                tx, ty = i1 - 1, i2 - 1
                top_left = grid[tx][ty]
            size = top_left + 1 if c2 == c1 else 0
            grid[i1][i2] = size
            if size >= substring_size:
                substring_size = size
                point = i1 + 1
    return s1[point - substring_size : point], substring_size


string, size = longest_common_substring(
    "my name is simon", "and i am faith and simon is my brother"
)
print(string, size)
