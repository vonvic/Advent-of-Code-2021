"""Advent of Code 2021 Problem 02 Code Solution."""

from typing import Tuple


def __run_moves(moves: list) -> Tuple[int, int]:
    """
    Return the final depth and horizontal position after running `moves`.

    For each move, it will have a distance and a direction. Depending on the
    direction, it will either modify the horizontal position or the depth.
    """
    depth = 0
    hor_pos = 0

    for move in moves:
        direction, distance = move
        match direction:
            case "forward":
                hor_pos += distance
            case "up":
                depth -= distance
            case "down":
                depth += distance
            case _:
                raise ValueError(f"Unknown direction {direction}")
    return (depth, hor_pos)


def __run_moves_with_aim(moves: list) -> Tuple[int, int]:
    """
    Return the final depth and horizontal position after running `moves`.

    For each move, it will have a distance and a direction. Depending on the
    direction, it will either modify the horizontal position, depth, or aim.
    The aim is only modified by directions `up` and `down`, while the depth
    and horizontal position is only modified by the `forward` direction.
    """
    depth = 0
    hor_pos = 0
    aim = 0

    for move in moves:
        direction, distance = move
        match direction:
            case "forward":
                hor_pos += distance
                depth += distance * aim
            case "up":
                aim -= distance
            case "down":
                aim += distance
            case _:
                raise ValueError(f"Unknown direction {direction}")
    return (depth, hor_pos)


def __convert_to_tuple(s: str) -> Tuple[int, int]:
    """Return a tuple of direction and distance as integers from `s`."""
    direction, distance = s.strip().split(" ")
    return (direction, int(distance))


def part_one_answer() -> int:
    """Return the part one answer."""
    depth, horizontal_position = __run_moves(__moves)
    return depth * horizontal_position


def part_two_answer() -> int:
    """Return the part two answer."""
    depth, horizontal_position = __run_moves_with_aim(__moves)
    return depth * horizontal_position


__moves: list
with open("02/input.txt", "r") as f:
    __moves = [__convert_to_tuple(line) for line in f.readlines()]
