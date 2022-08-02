"""
Description: Solution for Advent of Code 2021 Day 19.

Author: Cayas, Von Vic
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import FrozenSet, MutableSet


def _cos(theta: int) -> int:
    """Return the cosine at angles only of the degrees 0, 90, 180, and 279."""
    match theta:
        case 0:
            return 1
        case 90:
            return 0
        case 180:
            return -1
        case 270:
            return 0
        case _:
            raise ValueError(f"Unsupported angle {theta}")


def _sin(theta: int) -> int:
    """Return the sine at angles only of the degrees 0, 90, 180, and 279."""
    match theta:
        case 0:
            return 0
        case 90:
            return 1
        case 180:
            return 0
        case 270:
            return -1
        case _:
            raise ValueError(f"Unsupported angle {theta}")


@dataclass(frozen=True)
class Coordinate:
    """A coordinate class in three dimensions."""

    x: int
    y: int
    z: int

    def rotateZ(self, theta: int) -> Coordinate:
        """Return a Coordinate object of self rotated about the Z-axis."""
        x_prime = int(self.x * _cos(theta) - self.y * _sin(theta))
        y_prime = int(self.x * _sin(theta) + self.y * _cos(theta))
        z_prime = int(self.z)
        return Coordinate(x_prime, y_prime, z_prime)

    def rotateY(self, theta: int) -> Coordinate:
        """Return a Coordinate object of self rotated about the Y-axis."""
        x_prime = int(self.x * _cos(theta) + self.z * _sin(theta))
        y_prime = int(self.y)
        z_prime = int(-self.x * _sin(theta) + self.z * _cos(theta))
        return Coordinate(x_prime, y_prime, z_prime)

    def rotateX(self, theta: int) -> Coordinate:
        """Return a Coordinate object of self rotated about the X-axis."""
        x_prime = int(self.x)
        y_prime = int(self.y * _cos(theta) - self.z * _sin(theta))
        z_prime = int(self.y * _cos(theta) + self.z * _sin(theta))
        return Coordinate(x_prime, y_prime, z_prime)


@dataclass(frozen=True)
class Scanner:
    """A Scanner class that holds a set of all detected beacons."""

    beacons: FrozenSet[Coordinate]

    def __rotateAxis(self, theta: int, rotate: str) -> Scanner:
        """Rotate all the beacons about some axis of `theta` degrees."""
        rotated_beacons: MutableSet[Coordinate] = set()
        match rotate.lower():
            case "x":
                for beacon in self.beacons:
                    rotated_beacons.add(beacon.rotateX(theta))
            case "y":
                for beacon in self.beacons:
                    rotated_beacons.add(beacon.rotateY(theta))
            case "z":
                for beacon in self.beacons:
                    rotated_beacons.add(beacon.rotateZ(theta))
        return Scanner(frozenset(rotated_beacons))

    def rotateX(self, theta) -> Scanner:
        """Rotate all the beacons about the X axis of `theta` degrees."""
        return self.__rotateAxis(theta, "x")

    def rotateY(self, theta) -> Scanner:
        """Rotate all the beacons about the Y axis of `theta` degrees."""
        return self.__rotateAxis(theta, "y")

    def rotateZ(self, theta) -> Scanner:
        """Rotate all the beacons about the Z axis of `theta` degrees."""
        return self.__rotateAxis(theta, "z")


def get_scanners(filename: str) -> MutableSet[Scanner]:
    """
    Return a set of Scanner objects.

    Each Scanner object contains all the beacon coordinates specified in
    `filename`.
    """
    scanners: set[Scanner] = set()

    with open(filename, "r") as f:
        line = f.readline()

        beacons: MutableSet[Coordinate] = set()
        while line:
            line = (
                line[:-1] if line[-1] == "\n" else line
            )  # removes the new line character
            if line == "":
                scanners.add(Scanner(frozenset(beacons)))
            elif re.match(r"--- scanner .* ---", line):
                beacons = set()
            else:
                x, y, z = (int(n) for n in line.split(","))
                beacons.add(Coordinate(x, y, z))

            line = f.readline()

    if len(beacons) > 0:
        scanners.add(Scanner(frozenset(beacons)))

    return scanners


def main():
    """
    Display the answer for part 1 and part 2.

    As of right now, it tests functions as a solution hasn't been formulated
    yet.
    """
    # scanners = get_scanners('one.txt')

    scanner = Scanner(frozenset({Coordinate(1, 1, 1)}))

    rotated_scanners: MutableSet[Scanner] = set()
    for x_delta in range(0, 4):
        x_theta = x_delta * 90
        for y_delta in range(0, 4):
            y_theta = y_delta * 90
            for z_delta in range(0, 4):
                z_theta = z_delta * 90

                rotated_scanners.add(
                    scanner.rotateX(x_theta).rotateY(y_theta).rotateZ(z_theta)
                )

    for rotated in rotated_scanners:
        for beacon in rotated.beacons:
            print(beacon)

    # for scanner in scanners:
    #     print()
    #     for beacon in scanner.beacons:
    #         print(beacon)


if __name__ == "__main__":
    main()
