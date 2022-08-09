"""Advent of Code 2021 Problem 03 Code Solution."""

import re
from typing import Tuple


def __gamma_and_epsilon(diagnostics: list) -> Tuple[float, float]:
    """
    Return the gamma and epsilon calculated from diagnostics.

    From the diagnostics, columns are added together as an array (where 1 is
    treated as +1 and 0 is treated as -1). Then, the gamma is built by
    converting the array where positive values are 1s and negative values are
    0s. Likewise, epsilon is calculated similarly but switching 1s and 0s.
    """
    gamma: str
    epsilon: str

    bits = [0 for _ in range(len(diagnostics[0]))]

    for diagnostic in diagnostics:
        for i, bit in enumerate(diagnostic):
            bits[i] += 1 if bit == "1" else -1

    gamma = "".join(map(lambda x: "1" if x > 0 else "0", bits))
    gamma = int(gamma, 2)
    epsilon = "".join(map(lambda x: "0" if x > 0 else "1", bits))
    epsilon = int(epsilon, 2)

    return (gamma, epsilon)


def __get_o2_generator_and_co2_scrubber(diagnostics: list) -> Tuple[int, int]:
    """
    Calculate the oxygen generator and CO2 scubber from diagnostics.

    The oxygen generator is calculated by determining the most common value in
    each bit position, with 1 being the tiebreaker.

    The CO2 scrubbber is calculated by determining the least common value in
    each bit position, with 0 being the tiebreaker.
    """
    o2_gen = __get_oxygen_generator(__diagnostics)
    co2_gen = __get_co2_scrubber(__diagnostics)
    return o2_gen, co2_gen


def __get_oxygen_generator(diagnostics: list) -> int:
    """
    Calculate the oxygen generator value from diagnostics.

    The oxygen generator is calculated by determining the most common value in
    each bit position, with 1 being the tiebreaker.
    """
    count = [0 for _ in range(len(diagnostics[0]))]

    s = ""
    for i in range(len(count)):
        matched_count, matched_s = 0, ""
        for diagnostic in diagnostics:
            if re.match(s, diagnostic):
                matched_count += 1
                matched_s = diagnostic
                count[i] += 1 if diagnostic[i] == "1" else -1
        if matched_count == 1:
            s = matched_s
            break
        s += "1" if count[i] >= 0 else "0"

    return int(s, 2)


def __get_co2_scrubber(diagnostics: list) -> int:
    """
    Calculate the CO2 Scrubber value from diagnostics.

    The CO2 scrubbber is calculated by determining the least common value in
    each bit position, with 0 being the tiebreaker.
    """
    count = [0 for _ in range(len(diagnostics[0]))]

    s = ""
    for i in range(len(count)):
        matched_count, matched_s = 0, ""
        for diagnostic in diagnostics:
            if re.match(s, diagnostic):
                matched_count += 1
                matched_s = diagnostic
                count[i] += 1 if diagnostic[i] == "1" else -1
        if matched_count == 1:
            s = matched_s
            break
        s += "0" if count[i] >= 0 else "1"

    return int(s, 2)


def part_one_answer() -> int:
    """Return the product of gamma and epsilon of __diagnostics."""
    gamma, epsilon = __gamma_and_epsilon(__diagnostics)
    return gamma * epsilon


def part_two_answer() -> int:
    """Return the product of O2 generator and CO2 Scrubber."""
    o2_gen, co2_scrubber = __get_o2_generator_and_co2_scrubber(__diagnostics)
    return o2_gen * co2_scrubber


__diagnostics: list
with open("03/input.txt", "r") as f:
    __diagnostics = [x.strip() for x in f.readlines()]
