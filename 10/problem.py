"""Advent of Code 2021 Problem 10 Code Solution."""

MATCH_TABLE = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CORRUPT_SCORE_TABLE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

INCOMPLETE_SCORE_TABLE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def __count_corrupted(seqs: list) -> int:
    """
    Return the corrupted score of `seqs`.

    A corrupted line is a line with an illegal character in the chunk sequence.
    """
    score = 0
    for seq in seqs:
        character_stack = []
        for char in seq:
            if char in "([{<":
                character_stack.append(char)
                continue

            top = character_stack.pop()
            if MATCH_TABLE[top] != char:
                score += CORRUPT_SCORE_TABLE[char]
                break
    return score


def __count_incomplete(seqs: list) -> int:
    """
    Return the incomplete score of `seqs`.

    An imcomplete line is a line with missing matching characters in the chunk
    sequence.
    """
    from functools import reduce
    from statistics import median

    scores = []

    def f(p, x):
        """
        Return the calculation from previous `p` with current `x`.

        This is to be used in the reduce function.
        """
        return 5 * p + INCOMPLETE_SCORE_TABLE[MATCH_TABLE[x]]

    for seq in seqs:
        character_stack = []

        is_corrupted = False
        for char in seq:
            if char in "([{<":
                character_stack.append(char)
                continue

            top = character_stack.pop()
            if MATCH_TABLE[top] != char:
                is_corrupted = True
                break
        if is_corrupted:
            continue

        score = reduce(f, reversed(character_stack), 0)
        scores.append(score)
    return median(scores)


def __get_sequences(filename: str) -> list:
    """Retrieve the sequences defined in `filename`."""
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]


def part_one_answer() -> int:
    """Return part one answer."""
    return __count_corrupted(__sequences)


def part_two_answer() -> int:
    """Return part two answer."""
    return __count_incomplete(__sequences)


__sequences = __get_sequences("10/input.txt")
