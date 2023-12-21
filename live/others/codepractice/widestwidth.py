# Given n points on a 2D plane where points[i] = [xi, yi],
# Return the widest vertical area between two points such
# that no points are inside the area.

# A vertical area is an area of fixed-width extending
# infinitely along the y-axis (i.e., infinite height).
# The widest vertical area is the one with the maximum width.

# Note that points on the edge of a vertical area are not
# considered included in the area.

Point2D = tuple[int, int]


class Solution:
    def maxWidthOfVerticalArea(self, points: list[Point2D]) -> int:
        points.sort(key=lambda p: p[0])
        max_area: int = 0
        for i in range(1, len(points)):
            if (area := points[i][0] - points[i - 1][0]) > max_area:
                max_area = area
        return max_area
