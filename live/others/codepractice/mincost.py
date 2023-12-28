"""
Alice has n balloons arranged on a rope.
You are given a 0-indexed string colors
where colors[i] is the color of the ith
balloon.

Alice wants the rope to be colorful. She
does not want two consecutive balloons to
be of the same color, so she asks Bob for
help. Bob can remove some balloons from
the rope to make it colorful. You are given
a 0-indexed integer array neededTime where
neededTime[i] is the time (in seconds) that
Bob needs to remove the ith balloon from the
rope.

Return the minimum time Bob needs to make
the rope colorful.
"""

from random import choices
from typing import Sequence


class Solution:
    def minCost(self, colors: str, costs: Sequence[int]) -> int:
        size, index, min_costs = len(colors), 0, 0
        while index < size:
            current_color, max_cost = colors[index], 0
            total_cost, count = 0, 0
            while index < size:
                color = colors[index]
                if color != current_color: break
                cost = costs[index]
                count, index = count + 1, index + 1
                total_cost += cost
                max_cost = cost if cost > max_cost else max_cost
            min_costs += (total_cost - max_cost) if count > 1 else 0
        return min_costs


class TestCase:
    def __init__(
        self,
        size: int = 5,
        /,
        *,
        costs: Sequence[int] | None = None,
        colors: str | None = None,
    ):
        self.costs = choices(range(1, 5), k=size) if costs is None else costs
        self.colors = (
            "".join(chr(char) for char in choices(range(97, 103), k=size))
            if colors is None
            else colors
        )
        assert len(self.costs) == len(self.colors), (
            "Expected one-by-one match on colors and costs, but got "
            f"colors={self.colors!r} at [{len(self.colors or [])}] and"
            f"costs={self.costs} at [{len(self.costs)}]"
        )
        self.cost = self._cost()

    def _cost(self) -> int:
        return Solution().minCost(self.colors, self.costs)

    def __str__(self) -> str:
        return f"TestCase(colors={self.colors!r}, costs={self.costs!r}, cost={self.cost!r})"

    __repr__ = __str__


def main():
    cases: Sequence[tuple[str, Sequence[int], int]] = (
        ("", (), 0),
        ("a", (2,), 0),
        ("aa", (1, 2), 1),
        ("abb", (1, 2, 3), 2),
        ("aab", (2, 1, 3), 1),
        ("abc", (1, 2, 3), 0),
        ("abbc", (1, 2, 4, 3), 2),
        ("aaaaa", (2, 4, 5, 1, 3), 10),
        ("aabcc", (2, 1, 3, 4, 5), 5),
        ("aabaa", (1, 2, 3, 5, 4), 5),
        ("bbbbbc", (2, 4, 5, 1, 3, 6), 10),
        ("baaaaa", (1, 4, 3, 2, 5, 6), 14),
        ("aabbcc", (1, 2, 4, 3, 5, 6), 9),
        ("abccde", (1, 2, 3, 4, 5, 6), 3),
        ("bbbaaa", (4, 9, 3, 8, 8, 9), 23),
        ("baaaaac", (1, 2, 3, 4, 5, 6, 7), 14),
        ("baaaaacc", (1, 2, 3, 4, 5, 6, 7, 8), 21),
        ("aabcddfhh", (1, 2, 3, 4, 5, 6, 7, 4, 5), 10),
        ("cccebbbaaa", (2, 1, 3, 4, 9, 3, 8, 8, 9, 4), 26),
        ("abaddccaeefghh", (1, 2, 3, 2, 3, 4, 3, 2, 1, 2, 3, 4, 2, 3), 8),
        ("abbcccddddeeeee", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), 85),
        ("rggbbbrrrrgrggggg", (1, 2, 3, 4, 3, 2, 5, 2, 3, 1, 3, 5, 4, 2, 2, 4, 5), 25),
    )

    from rich import print

    for colors, costs, cost in cases:
        testcase = TestCase(costs=costs, colors=colors)
        print(
            f"[green]PASSED[white]: [blue][underline]testcase[/underline][white]=[yellow]{testcase}"
            if testcase.cost == cost
            else (
                "[red]FAILED[white]: [blue][underline]testcase[/underline][white]=[yellow]"
                f"{testcase}[white], expected [blue][underline]cost[/underline][white]=[yellow]{cost}"
            )
        )


if __name__ == "__main__":
    main()
