from typing import Counter

class Solution:
    braces = {'(':')', '{':'}', '[':']'}

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
            if brace in self.braces: trace.append(brace)
            elif not trace or self.braces[trace.pop()] != brace:
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
        return Counter(s) == Counter(t)


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