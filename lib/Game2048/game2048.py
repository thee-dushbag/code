import copy
import random
from typing import Any, Literal

from .util import AdjacentOperate


class Game2048:
    def __init__(self, dim: int = 5, hscore: int = 2048) -> None:
        self.new_game(hscore=hscore, dim=dim)

    def new_game(self, hscore: int = 2048, dim: int = 5) -> None:
        self.dim: int = dim
        self.matrix: list[list[int]] = [
            [0 for _ in range(self.dim)] for _ in range(self.dim)
        ]
        self.score: Literal[0] = 0
        self.hscore: int = hscore
        self.highest: Literal[0] = 0
        self.hscore_reached: bool = False
        self.insert_new_item()
        self.insert_new_item()

    def __rotate_90deg_clockwise(self, matr: list[list[int]]) -> list[list[int]]:  # type: ignore
        columns: list[list[int]] = [
            [row[column_index] for row in matr] for column_index in range(self.dim)
        ]
        matr: list[list[int]] = [list(reversed(column)) for column in columns]
        return matr

    def rotate_90deg_clockwise(self) -> None:
        self.matrix = self.__rotate_90deg_clockwise(self.matrix)

    def set_highest(self) -> None:
        highest: Literal[0] = 0
        for row in self.matrix:
            if max(row) > highest:
                highest = max(row)  # type: ignore
        if highest >= self.hscore:
            self.hscore_reached = True
        self.highest = highest

    def score_keeper(self, value) -> None:
        weight = value * 2
        self.score += weight
        return weight

    def merge_row(self, obj: list[int], __f: int = 0) -> list[int]:  # type: ignore
        obj = [x for x in obj if x != __f]
        obj: list[int] = AdjacentOperate(obj, self.score_keeper)
        self.__fill_dim(obj)
        return obj

    def __fill_dim(self, obj: list[Any], __filler: int = 0) -> None:
        while len(obj) != self.dim:
            obj.append(__filler)

    def check_game_over(self) -> bool:
        cmatrix: list[list[int]] = copy.deepcopy(self.matrix)
        # check if hscore has been reached.
        self.set_highest()
        if self.hscore_reached:
            return True
        # check if left slidable
        dmatrix: list[list[int]] = self.__slide_left(copy.copy(cmatrix))
        if not self.compare_matrix(dmatrix, self.matrix):
            return False
        # check if up slidable
        dmatrix = self.__slide_right(copy.copy(cmatrix))
        if not self.compare_matrix(dmatrix, self.matrix):
            return False
        # check if right slidable
        dmatrix = self.__slide_up(copy.copy(cmatrix))
        if not self.compare_matrix(dmatrix, self.matrix):
            return False
        # check if down slidable
        dmatrix = self.__slide_down(copy.copy(cmatrix))
        if not self.compare_matrix(dmatrix, self.matrix):
            return False
        return True

    @staticmethod
    def compare_matrix(matrix1, matrix2) -> bool:
        for row1, row2 in zip(matrix1, matrix2):
            for val1, val2 in zip(row1, row2):
                if val1 != val2:
                    return False
        return True

    def slide_left(self) -> None:
        self.__slide_left(self.matrix)
        self.insert_new_item()

    def slide_right(self) -> None:
        self.matrix = self.__slide_right(self.matrix)
        self.insert_new_item()

    def slide_up(self) -> None:
        self.matrix = self.__slide_up(self.matrix)
        self.insert_new_item()

    def slide_down(self) -> None:
        self.matrix = self.__slide_down(self.matrix)
        self.insert_new_item()

    def get_empty(self) -> list[list[int]]:
        return [
            [x, y]
            for x in range(self.dim)
            for y in range(self.dim)
            if self.matrix[x][y] == 0
        ]

    def insert_new_item(self, value: int = 2) -> None:
        if empty_spots := self.get_empty():
            rindex: list[int] = random.choice(empty_spots)
            self.matrix[rindex[0]][rindex[1]] = value

    def __slide_left(self, matrix: list[list[int]]) -> list[list[int]]:
        for index in range(len(matrix)):
            matrix[index] = self.merge_row(matrix[index])
        return matrix

    def __slide_right(self, matrix: list[list[int]]) -> list[list[int]]:  # type: ignore
        matrix: list[list[int]] = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__slide_left(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        return matrix

    def __slide_down(self, matrix) -> list[list[int]]:  # type: ignore
        matrix: list[list[int]] = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__slide_left(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        return matrix

    def __slide_up(self, matrix) -> list[list[int]]:  # type: ignore
        matrix: list[list[int]] = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        matrix = self.__slide_left(matrix)
        matrix = self.__rotate_90deg_clockwise(matrix)
        return matrix
