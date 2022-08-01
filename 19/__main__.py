from typing import FrozenSet, MutableSet
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Coordinate:
    """Simple coordinate class in three dimensions."""
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Scanner:
    """A Scanner class that holds a set of all detected beacons"""
    beacons: FrozenSet[Coordinate]


def get_scanners(filename: str) -> FrozenSet[Scanner]:
    """Returns a set of Scanner objects, each which contain all the beacon coordinates specified in
    `filename`."""
    scanners: set[Scanner] = set()

    with open(filename, 'r') as f:
        line = f.readline()

        beacons: MutableSet[Coordinate] = set()
        while line:
            line = line[:-1] # removes the new line character
            if line == '':
                scanners.add(Scanner(frozenset(beacons)))
            elif re.match(r'--- scanner .* ---', line):
                beacons = set()
            else:
                x, y, z = (int(n) for n in line.split(','))
                beacons.add(Coordinate(x, y, z))
            
            line = f.readline()

    return scanners


def main():
    scanners = get_scanners('sample.txt')
    for scanner in scanners:
        print()
        for beacon in scanner.beacons:
            print(beacon)

if __name__ == '__main__':
    main()