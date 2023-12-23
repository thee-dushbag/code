import typing as ty


class Solution:
    _braces = {"(": ")", "{": "}", "[": "]"}

    def maxProductDifference(self, nums: list[int]) -> int:
        """
        The product difference between two pairs (a, b) and
        (c, d) is defined as (a * b) - (c * d).

        For example, the product difference between (5, 6)
        and (2, 7) is (5 * 6) - (2 * 7) = 16.
        Given an integer array nums, choose four distinct
        indices w, x, y, and z such that the product difference
        between pairs (nums[w], nums[x]) and (nums[y], nums[z])
        is maximized.

        Return the maximum such product difference.
        """
        nums.sort()
        return nums[-1] * nums[-2] - nums[0] * nums[1]

    def isValid(self, s: str) -> bool:
        """
        Given a string s containing just the characters
        '(', ')', '{', '}', '[' and ']', determine if
        the input string is valid.

        An input string is valid if:
        -> Open brackets must be closed by the same type of brackets.
        -> Open brackets must be closed in the correct order.
        -> Every close bracket has a corresponding open bracket of the same type.
        """
        trace = []
        for brace in s:
            if brace in self._braces:
                trace.append(brace)
            elif not trace or self._braces[trace.pop()] != brace:
                return False
        return not trace

    def isAnagram(self, s: str, t: str) -> bool:
        """
        Given two strings s and t, return true if t is an
        anagram of s, and false otherwise.

        An Anagram is a word or phrase formed by rearranging
        the letters of a different word or phrase, typically
        using all the original letters exactly once.
        """
        return ty.Counter(s) == ty.Counter(t)

    def destCity(self, paths: list[list[str]]) -> str:
        """
        You are given the array paths, where paths[i] = [cityAi, cityBi]
        means there exists a direct path going from cityAi to cityBi.
        Return the destination city, that is, the city without any path
        outgoing to another city.

        It is guaranteed that the graph of paths forms a line without
        any loop, therefore, there will be exactly one destination city.
        """
        return ({c for ct in paths for c in ct} - {o for o, _ in paths}).pop()

    def maxScore(self, s: str) -> int:
        """
        Given a string s of zeros and ones, return the maximum score
        after splitting the string into two non-empty substrings (i.e.
        left substring and right substring).

        The score after splitting a string is the number of zeros in
        the left substring plus the number of ones in the right substring.
        """
        max_score = score = (s[0] == "0") + s[1:].count("1")
        for bit in map(int, s[1:-1]):
            score += not bit or -1
            if score > max_score:
                max_score = score
        return max_score

    _step: ty.Callable[[str], tuple[int, int]] = staticmethod(
        dict(
            N=(0, 1),
            S=(0, -1),
            E=(1, 0),
            W=(-1, 0),
        ).__getitem__
    )

    def isPathCrossing(self, path: str) -> bool:
        current: tuple[int, int] = 0, 0
        passed: set[tuple[int, int]] = {current}
        for step in map(self._step, path):
            current = current[0] + step[0], current[1] + step[1]
            if current in passed:
                return True
            passed.add(current)
        return False
