"""Advent of Code 2021 Problem 05 Code Solution."""

from typing import List, Tuple


def __get_dimensions(segments: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Return the minimum dimensions of the square that contain `segments`."""
    max_x, max_y = 0, 0

    for segment in segments:
        one, two = segment
        x1, y1 = one
        x2, y2 = two
        max_x, max_y = max(max_x, x1, x2), max(max_y, y1, y2)

    return (max_x + 1, max_y + 1)


def __get_segments(
    lines: List[str],
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Return a list of segments defined by each line in `lines.

    A segment is defined as a tuple of two points in cartesian space.
    """

    def convert_to_tuple(x: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        one, two = [y.strip() for y in x.split("->")]
        start = tuple([int(z) for z in one.split(",")])
        end = tuple([int(z) for z in two.split(",")])
        return start, end

    segments = [convert_to_tuple(x.strip()) for x in lines]
    return segments


def __build_matrix(dimensions: Tuple[int, int]) -> List[List[int]]:
    """Return a matrix of size `dimensions` with each value set to 0."""
    x, y = dimensions
    matrix = []
    for _ in range(y):
        matrix.append([0 for _ in range(x)])
    return matrix


def __lay_segments(
    segments: List[Tuple[int, int]],
    matrix: List[List[int]],
    diagonal: bool = True,
) -> None:
    """
    Place every segment from `segments` on `matrix`.

    Placing a segment on `matrix` will increase the values on that matrix that
    the segment is on by 1. Therefore, if two segments intersect, the
    intersection point will increase by 2.
    """
    for segment in segments:
        one, two = segment
        x1, y1 = one
        x2, y2 = two

        if x1 == x2:  # vertical
            for i in range(abs(y2 - y1) + 1):
                matrix[min(y1, y2) + i][x1] += 1
        elif y1 == y2:  # horizontal
            for i in range(abs(x2 - x1) + 1):
                matrix[y1][min(x1, x2) + i] += 1
        else:  # diagonal
            if diagonal:
                x_delta = 1 if x2 > x1 else -1
                y_delta = 1 if y2 > y1 else -1
                for i in range(abs(y2 - y1) + 1):
                    matrix[y1 + y_delta * i][x1 + x_delta * i] += 1
                pass


def __output_matrix(matrix: list, out_name: str):
    """Output the matrix into a file called `out_name`."""
    with open(out_name, "w") as f:
        for row in matrix:
            f.write(" ".join([str(x) for x in row]) + "\n")


def __get_overlapping_count(matrix: list) -> int:
    """
    Return the number of points that two segments lay on in `matrix`.

    An overlapping is defined to be a point on the matrix with a value greater
    than one.
    """
    count = 0
    for row in matrix:
        for val in row:
            if val > 1:
                count += 1
    return count


def part_one_answer() -> int:
    """Return part one answer."""
    matrix = __build_matrix(__dimensions)
    __lay_segments(__segments, matrix, diagonal=False)
    overlapping_count = __get_overlapping_count(matrix)
    return overlapping_count


def part_two_answer() -> int:
    """Return part two answer."""
    matrix = __build_matrix(__dimensions)
    __lay_segments(__segments, matrix)
    overlapping_count = __get_overlapping_count(matrix)
    return overlapping_count


__segments: list
with open("05/input.txt", "r") as f:
    __segments = __get_segments(f.readlines())
__dimensions = __get_dimensions(__segments)
