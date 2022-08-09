"""Advent of Code 2021 Problem 15 Code Solution."""

from __future__ import annotations

from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])


class _Matrix:
    def __init__(self, matrix: list[list[int]]):
        self._matrix = matrix
        self._marked = set()

    @property
    def row_count(self):
        return len(self._matrix)

    @property
    def col_count(self):
        return len(self._matrix[0])

    @property
    def rows(self):
        return self._matrix

    def at(self, position: Position):
        return self._matrix[position.y][position.x]

    def mark(self, position: Position):
        self._marked.add(position)

    def copy(self) -> _Matrix:
        matrix_copy = []
        for row in self._matrix:
            matrix_copy.append(row.copy())
        return _Matrix(matrix_copy)

    def increase_all(self, N):
        for i, row in enumerate(self._matrix):
            self._matrix[i] = [
                (x + N) % 9 if (x + N) % 9 != 0 else 9 for x in row
            ]

    def __str__(self):
        s = ""

        for y, row in enumerate(self._matrix):
            for x, val in enumerate(row):
                s += str(val)
            s += "\n"
        return s[:-1]

    def __repr__(self):
        return str(self)


def __get_map(filename: str) -> _Matrix:
    """Return a matrix specified by matrix values in `filename`."""
    matrix: list[list[int]] = []

    with open(filename, "r") as f:
        for line in map(str.strip, f.readlines()):
            matrix.append([int(x) for x in line])

    return _Matrix(matrix)


def __get_full_map(original: _Matrix) -> _Matrix:
    """
    Return the full version of `original`, increased by a factor of 5.

    Each copy of `original` immediately to the right and down of `original`
    have each value increased by 1. If the new value is greater than 9, then
    that value is reset by modulo 9.
    """
    new_matrix = []
    for _ in range(original.row_count * 5):
        new_matrix.append([0 for _ in range(original.col_count * 5)])

    for y, row in enumerate(original.rows):
        for x, val in enumerate(row):
            for i in range(5):
                for j in range(5):
                    curr_x = x + j * original.col_count
                    curr_y = y + i * original.row_count
                    new_val = (
                        (val + (i + j)) % 9 if (val + (i + j)) % 9 != 0 else 9
                    )
                    new_matrix[curr_y][curr_x] = new_val

    return _Matrix(new_matrix)


def __get_next_positions(matrix: _Matrix, position: Position):
    """Return a valid collection of next positions at `position` in `matrix."""
    positions = [
        Position(position.x, position.y - 1),
        Position(position.x, position.y + 1),
        Position(position.x - 1, position.y),
        Position(position.x + 1, position.y),
    ]

    def valid_position(p: Position) -> bool:
        """Return True if `p` is a valid position in `matrix`. Else, False."""
        return 0 <= p.x < matrix.count and 0 <= p.y < matrix.row_count

    return filter(valid_position, positions)


def __find_lowest_risk_path(matrix: _Matrix):
    """Return the lowest risk of a path from the top to bottom of `matrix`."""
    """Returns the value of the lowest risk path by using the A* search
    algorithm."""
    Node = namedtuple("Node", ["cost", "position"])

    start = Position(x=0, y=0)
    goal = Position(x=matrix.col_count - 1, y=matrix.row_count - 1)

    def heuristic(p1: Position, p2: Position) -> float:
        return abs(p1.x - p1.y) + abs(p2.x - p2.y)

    def f(node: Node) -> float:
        # return node.cost + heuristic(node.position, goal)
        return node.cost

    current_node = Node(0, start)
    frontier = {current_node}
    discovered = {current_node.position}
    while frontier:
        best_node = min(frontier, key=f)
        frontier.remove(best_node)
        if best_node.position == goal:
            current_node = best_node
            break

        for position in __get_next_positions(matrix, best_node.position):
            if position not in discovered:
                new_cost = best_node.cost + matrix.at(position)
                new_node = Node(new_cost, position)
                frontier.add(new_node)
                discovered.add(position)
        current_node = best_node
    return current_node.cost


def part_one_answer() -> int:
    """Return part one answer."""
    return __find_lowest_risk_path(__matrix)


def part_two_answer() -> int:
    """Return part two answer."""
    full_map = __get_full_map(__matrix)
    return __find_lowest_risk_path(full_map)


__matrix = __get_map("15/input.txt")
