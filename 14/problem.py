"""Advent of Code 2021 Problem 14 Code Solution."""

from typing import Dict, Tuple


def __get_template_and_rules(filename: str) -> Tuple[str, Dict[str, str]]:
    """
    Return the template and rules as defined in `filename`.

    The template is first line of the file and rules is the rest of the lines
    in that file (after the blank line).'''
    """
    template: str
    rules = dict()
    with open(filename, "r") as f:
        template = f.readline().strip()
        f.readline()  # blank line
        for rule in f.readlines():
            k, v = rule.split(" -> ")
            rules[k] = v.strip()
    return (template, rules)


def __get_freq_table_after_running(template: str, rules: dict, N: int):
    """
    Return the frequency of table after running `rules` against `template`.

    `rules` will be ran against `template` `N` times.
    """
    from collections import Counter
    from itertools import pairwise

    pairs_freq = Counter(map("".join, pairwise(template)))

    letter_freq = Counter(template)
    for _ in range(N):
        new_counter = Counter()
        for pair, freq in pairs_freq.items():
            c = rules[pair]
            l, r = pair
            new_counter[l + c] += freq
            new_counter[c + r] += freq
            letter_freq[c] += freq
        pairs_freq = new_counter
    return letter_freq


def __get_most_and_least_count(freq: dict) -> Tuple[int, int]:
    """Return the most and least frequent of `freq`."""
    most_freq, least_freq = max(freq, key=freq.get), min(freq, key=freq.get)
    return freq[most_freq], freq[least_freq]


def part_one_answer() -> int:
    """Return part one answer."""
    N = 10
    freq = __get_freq_table_after_running(__template, __rules, N)
    most, least = __get_most_and_least_count(freq)
    return most - least


def part_two_answer() -> int:
    """Return part two answer."""
    N = 40
    freq = __get_freq_table_after_running(__template, __rules, N)
    most, least = most, least = __get_most_and_least_count(freq)
    return most - least


__template, __rules = __get_template_and_rules("14/input.txt")
