"""Advent of Code 2021 Problem 07 Code Solution."""


def __get_target_one(L: list):
    """Return the median of the list."""
    from statistics import median

    return int(median(L))


def __get_target_two(L: list) -> int:
    """Return the mean of `L` rounded down to the nearest integer."""
    from statistics import mean

    return int(mean(L))


def __calculate_fuel_one(L: list, target: int) -> int:
    """
    Calculate the minimum fuel needed to align all the crabs together.

    This minimum fuel is the sum of the absolute values between each value in
    `L` and `target`.
    """
    from functools import reduce

    return reduce(lambda p, x: p + abs(target - x), L, 0)


def __calculate_fuel_two(L: list, target: int) -> int:
    """
    Calculate the minimum fuel needed to align all the crabs together.

    This minimum fuel is the sum of the triangle numbers, where each triangle
    number is the defined by distance between each element in `L` and `target`.
    """
    from functools import reduce

    def f(p, x):
        diff = int(abs(x - target) + 1)
        value = diff * (diff - 1) // 2
        return p + value

    return reduce(f, L, 0)


def __get_list(file: str):
    """Return the list of the initial state of crab horizontal positions."""
    with open(file, "r") as f:
        return [int(x.strip()) for x in f.readline().split(",")]


def part_one_answer() -> int:
    """Return part one answer."""
    target = __get_target_one(__crabs)
    fuel = __calculate_fuel_one(__crabs, target)
    return fuel


def part_two_answer() -> int:
    """Return part two answer."""
    target_two = __get_target_two(__crabs)
    fuel_two = __calculate_fuel_two(__crabs, target_two)
    return fuel_two


__crabs = sorted(__get_list("07/input.txt"))
