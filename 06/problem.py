"""Advent of Code 2021 Problem 06 Code Solution."""

_OPT = dict()


def __simulate_lantern_fish(days_left: int, timer: int, timer_start: int):
    """
    Return the number of lantern fish after simulating for `days_left`.

    This is calculated with the fact that after `days_left` pass by for a
    single lantern fish, it births a new lantern fish after timer runs down to
    -1. Once the a baby is birthed, the timer restarts to timer_start to 6
    days. Each baby has a timer_start of 8 days.
    """
    param = (days_left, timer, timer_start)
    if param in _OPT:
        return _OPT[param]  # retrieve prev. saved value from memoization

    if days_left == -1:
        return 1

    if timer == -1:  # birth new baby
        curr_timer_start = 6
        baby_timer_start = 8
        curr = __simulate_lantern_fish(
            days_left - 1, curr_timer_start - 1, curr_timer_start
        )
        baby = __simulate_lantern_fish(
            days_left - 1, baby_timer_start - 1, baby_timer_start
        )

        _OPT[param] = curr + baby
        return _OPT[param]
    else:  # run down the timer and continue on days
        _OPT[param] = __simulate_lantern_fish(
            days_left - 1, timer - 1, timer_start
        )
        return _OPT[param]


def __get_list(file: str):
    """Return the list of the initial state of lantern fish."""
    with open(file, "r") as f:
        return [int(x.strip()) for x in f.readline().split(",")]


def part_one_answer() -> int:
    """Return part one answer."""
    total = 0
    timer_start = 6
    days_left = 80

    for fish in __lantern_fishes:
        total += __simulate_lantern_fish(days_left, fish, timer_start)

    return total


def part_two_answer() -> int:
    """Return part two answer."""
    total = 0
    timer_start = 6
    days_left = 256

    for fish in __lantern_fishes:
        total += __simulate_lantern_fish(days_left, fish, timer_start)

    return total


__lantern_fishes = __get_list("06/input.txt")
