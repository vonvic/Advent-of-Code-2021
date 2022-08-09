"""Advent of Code 2021 Problem 01 Code Solution."""

depths: list
with open("01/input.txt", "r") as f:
    depths = [int(line.strip()) for line in f.readlines()]


def __count_increases(depths: list, width: int = 0):
    """
    Return the # of measurements of n-len that are larger than its previous.

    Return the number of times the sum of depths increases from a previous
    measurement. The sum of depths is specified from the `width` argument.
    """
    count = 0
    for i in range(1, len(depths)):
        prev, curr = sum(depths[i - 1 : i - 1 + width + 1]), sum(  # noqa E203
            depths[i : i + width + 1]  # noqa E203
        )
        if (curr - prev) > 0:
            count += 1
    return count


def part_one_answer() -> int:
    """Return the number of measurements that are larger than its previous."""
    return __count_increases(depths)


def part_two_answer() -> int:
    """Return the number of sums of three that are larger than its previous."""
    return __count_increases(depths, 2)


if __name__ == "__main__":
    depths: list
    with open("input.txt", "r") as f:
        depths = [int(line.strip()) for line in f.readlines()]
