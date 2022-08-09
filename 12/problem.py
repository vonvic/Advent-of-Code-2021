"""Advent of Code 2021 Problem 12 Code Solution."""

from __future__ import annotations

from enum import Enum
from typing import List


class CaveType(Enum):
    """Defines the types of nodes in a cave system."""

    START = 0
    END = 1
    BIG = 2
    SMALL = 3


class Cave:
    """A node in a cave system."""

    def __init__(self, name: str, type: CaveType):
        """Initialize object with name, type, and empty list of connections."""
        self._name: str = name
        self._type: CaveType = type
        self._connections: List[Cave] = []

    def add_connected_cave(self, cave: Cave):
        """Add `cave` to list of connections to `self`."""
        self._connections.append(cave)

    @property
    def name(self) -> str:
        """Return the name of self."""
        return self._name

    @property
    def connections(self) -> List[Cave]:
        """Return the list of connections of `self`."""
        return self._connections

    @property
    def type(self) -> CaveType:
        """Return the cave type."""
        return self._type

    def __str__(self):
        """Return a list of connections prefixed by the name."""
        s = f"{self._name} : "
        connection: Cave
        for connection in self._connections:
            s += f"{connection.name} "
        return s[:-1]

    def __repr__(self):
        """Return the string representation of self."""
        return str(self)

    def __eq__(self, other):
        """Return the equivalency of this and other's name."""
        return self.name == other.name

    def __hash__(self):
        """Return the hash of the Caves name."""
        return hash(self.name)


def __load_connections(filename: str) -> list:
    """Return all the connections defined in `filename`."""
    connections = []

    with open(filename, "r") as f:
        for line in [line.strip() for line in f.readlines()]:
            connections.append(tuple(line.split("-")))

    return connections


def __evaluate_cave_type(s: str) -> CaveType:
    """Return the cave type as an enum from `s`."""
    match s:
        case "start":
            return CaveType.START
        case "end":
            return CaveType.END
        case _:
            return CaveType.BIG if s.isupper() else CaveType.SMALL


def __build_cave(connections: list) -> Cave:
    """Return the start of the cave connections built by `connections`."""
    nodes = dict()

    for A, B in connections:
        A_type: CaveType = __evaluate_cave_type(A)
        B_type: CaveType = __evaluate_cave_type(B)

        A_cave = nodes.get(A, Cave(A, A_type))
        B_cave = nodes.get(B, Cave(B, B_type))

        A_cave.add_connected_cave(B_cave)
        B_cave.add_connected_cave(A_cave)

        nodes[A] = A_cave
        nodes[B] = B_cave

    return nodes["start"]


def ____get_distinct_paths_rec(cave: Cave, visited: set = set()) -> list:
    """
    Return the number of distinct paths in the cave system starting at `cave`.

    Recursively traverses through all nodes connected with `cave`. Any
    adjacent connections that are already visited will not be traversed. The
    START cave will also not be visited. BIG caves can be visited more than
    once.
    """
    if cave.type is CaveType.END:
        return [[cave.name]]

    paths = []

    connection: Cave
    for connection in cave.connections:
        if connection in visited or connection.type is CaveType.START:
            continue

        if connection.type is CaveType.SMALL:
            visited.add(connection)
        connection_paths = ____get_distinct_paths_rec(connection, visited)
        if connection.type is CaveType.SMALL:
            visited.remove(connection)

        for path in connection_paths:
            paths.append([cave.name] + path)

    return paths


def __get_distinct_paths(cave_start: Cave) -> list:
    """
    Return the number of distinct paths in the cave system starting at `cave`.

    The list of all distinct paths starting at `cave_start` to a cave of
    type 'CaveType.END' is obtained by ____get_distinct_paths_rec.
    """
    paths = ____get_distinct_paths_rec(cave_start)
    return paths


def __get_distinct_new_paths_rec(
    cave: Cave, visited: set = set(), first_small_cave: Cave = None
) -> list:
    """
    Return the number of distinct new paths in the system starting at `cave`.

    Recursively traverses through all nodes connected with `cave`. Any
    adjacent connections that are already visited will not be traversed. The
    START cave will also not be visited. BIG caves can be visited more than
    once. Out of all small caves visited, only one of them can be visited at
    most twice. The rest of the small caves can be visited only at most once.
    """
    if cave.type is CaveType.END:
        return {(cave.name,)}

    paths = set()

    connection: Cave
    for connection in cave.connections:
        if connection in visited or connection.type is CaveType.START:
            continue

        new_first_small: Cave = first_small_cave
        if not new_first_small and connection.type is CaveType.SMALL:
            new_first_small = connection

        if first_small_cave and connection.type is CaveType.SMALL:
            visited.add(connection)
        connection_paths = __get_distinct_new_paths_rec(
            connection, visited, new_first_small
        )
        if first_small_cave and connection.type is CaveType.SMALL:
            visited.remove(connection)

        if not first_small_cave:
            if connection.type is CaveType.SMALL:
                visited.add(connection)
            connection_paths |= __get_distinct_new_paths_rec(
                connection, visited
            )
            if connection.type is CaveType.SMALL:
                visited.remove(connection)

        for path in connection_paths:
            paths.add((cave.name,) + path)

    return paths


def __get_distinct_new_paths(cave_start: Cave) -> list:
    """
    Return the number of distinct new paths in the system starting at `cave`.

    The list of all distinct paths starting at `cave_start` to a cave of
    type 'CaveType.END' with new rules is obtained through
    __get_distinct_new_paths_rec.
    """
    paths = __get_distinct_new_paths_rec(cave_start)
    return paths


def part_one_answer() -> int:
    """Return part one answer."""
    return len(__get_distinct_paths(__cave_start))


def part_two_answer() -> int:
    """Return part two answer."""
    return len(__get_distinct_new_paths(__cave_start))


__connections = __load_connections("12/input.txt")
__cave_start = __build_cave(__connections)
