"""Advent of Code 2021 Problem 09 Code Solution."""

from itertools import reduce


def get_low_points_loc(height_map) -> list:
    """
    Return a list of low points between in `height_map`.

    A low point is defined as a point in the height_map for which its vertical
    and horizontal neighbors are greater in value than itself.
    """
    low_points_loc = []
    for row in range(len(height_map)):
        for col in range(len(height_map[row])):
            this_val = height_map[row][col]
            hor_low_point, vert_low_point = True, True

            if col > 0:
                hor_low_point &= this_val < height_map[row][col - 1]
            if col < len(height_map[row]) - 1:
                hor_low_point &= this_val < height_map[row][col + 1]

            if row > 0:
                vert_low_point &= this_val < height_map[row - 1][col]
            if row < len(height_map) - 1:
                vert_low_point &= this_val < height_map[row + 1][col]

            if hor_low_point and vert_low_point:
                low_points_loc.append((row, col))
    return low_points_loc


def get_height_map(filename: str) -> tuple:
    """Return the height map as defined in `filename`."""
    height_map = []
    with open(filename, "r") as f:
        rows = [line.strip() for line in f.readlines()]
        for row in rows:
            height_map.append([int(height) for height in row])
    return height_map


def get_risk_levels(height_map, low_points_loc) -> list:
    """
    Return a list of risk levels from `height map`.

    A risk level is a low point in `height_map` increased by one.s
    """
    risk_levels = []
    for row, col in low_points_loc:
        risk_levels.append(height_map[row][col] + 1)
    return risk_levels


def get_basin_size_from_point(height_map, row, col) -> int:
    """
    Return the size of the basin that the point resides in.

    Traverses through the graph by manuevering through vertical and horizontal
    neighbors, with each value in the basin constituing as 1 of the total size.
    """
    value = height_map[row][col]
    if value == 9:
        return 0
    height_map[row][col] = 9

    is_left = value < height_map[row][col - 1] if col > 0 else False
    is_right = (
        value < height_map[row][col + 1]
        if col < len(height_map[row]) - 1
        else False
    )
    is_up = value < height_map[row - 1][col] if row > 0 else False
    is_down = (
        value < height_map[row + 1][col]
        if row < len(height_map) - 1
        else False
    )

    left = (
        get_basin_size_from_point(height_map, row, col - 1) if is_left else 0
    )
    right = (
        get_basin_size_from_point(height_map, row, col + 1) if is_right else 0
    )
    up = get_basin_size_from_point(height_map, row - 1, col) if is_up else 0
    down = (
        get_basin_size_from_point(height_map, row + 1, col) if is_down else 0
    )

    return left + right + up + down + 1


def get_basin_sizes(height_map, low_points_loc) -> list:
    """Return all the sizes of all the basins in `height_map`."""
    sizes = []

    for row, col in low_points_loc:
        sizes.append(get_basin_size_from_point(height_map, row, col))

    return sizes


def part_one_answer() -> int:
    """Return part one answer."""
    risk_levels = get_risk_levels(__height_map, __low_points_loc)
    return sum(risk_levels)


def part_two_answer() -> int:
    """Return part two answer."""
    basin_sizes = get_basin_sizes(__height_map, __low_points_loc)
    return reduce(lambda p, x: p * x, sorted(basin_sizes, reverse=True)[:3])


__height_map = get_height_map("09/input.txt")
__low_points_loc = get_low_points_loc(__height_map)
