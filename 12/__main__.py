from __future__ import annotations
from enum import Enum

class CaveType(Enum):
    START = 0
    END = 1
    BIG = 2
    SMALL = 3

class Cave:
    def __init__(self, name: str, type: CaveType):
        self._name = name
        self._type = type
        self._connections = []
    
    def add_connected_cave(self, cave: Cave):
        self._connections.append(cave)

    @property
    def name(self): return self._name

    @property
    def connections(self): return self._connections

    @property
    def type(self): return self._type

    def __str__(self):
        s = f'{self._name} : '
        connection: Cave
        for connection in self._connections: s += f'{connection.name} '
        return s[:-1]

    def __repr__(self): return str(self)

    def __eq__(self, other): return self.name == other.name
    def __hash__(self): return hash(self.name)

def load_connections(filename: str) -> list:
    '''Returns a list of tuples representing the undirected connections
    specified in `filename`.'''
    connections = []

    with open(filename, 'r') as f:
        for line in [line.strip() for line in f.readlines()]:
            connections.append(tuple(line.split('-')))

    return connections

def evaluate_cave_type(s: str) -> CaveType:
    '''Returns the cavetype by determining if `s` is 'start', 'end' or all upper
    or all lower.'''
    match s:
        case 'start': return CaveType.START
        case 'end': return CaveType.END
        case _: return CaveType.BIG if s.isupper() else CaveType.SMALL

def build_cave(connections: list) -> Cave:
    '''Returns the start of the cave connections built by `connections`.'''
    nodes = dict()

    for A, B in connections:
        A_type: CaveType = evaluate_cave_type(A)
        B_type: CaveType = evaluate_cave_type(B)

        A_cave = nodes.get(A, Cave(A, A_type))
        B_cave = nodes.get(B, Cave(B, B_type))

        A_cave.add_connected_cave(B_cave)
        B_cave.add_connected_cave(A_cave)

        nodes[A] = A_cave
        nodes[B] = B_cave

    return nodes['start']

def _get_distinct_paths(cave: Cave, visited: set = set()) -> list:
    '''Recursively traverses through all nodes connected with `cave`. Any
    adjacent connections that are already visited will not be traversed. The
    START cave will also not be visited. BIG caves can be visited more than
    once.'''
    if cave.type is CaveType.END: return [[cave.name]]

    paths = []

    connection: Cave
    for connection in cave.connections:
        if connection in visited or connection.type is CaveType.START: continue

        if connection.type is CaveType.SMALL: visited.add(connection)
        connection_paths = _get_distinct_paths(connection, visited)
        if connection.type is CaveType.SMALL: visited.remove(connection)

        for path in connection_paths: paths.append([cave.name] + path)

    return paths

def get_distinct_paths(cave_start: Cave) -> list:
    '''Returns a list of all distinct paths starting at `cave_start` to a cave of
    type 'CaveType.END'.'''
    paths = _get_distinct_paths(cave_start)
    return paths

def _get_distinct_new_paths(cave: Cave, visited: set = set(), first_small_cave: Cave = None) -> list:
    '''Recursively traverses through all nodes connected with `cave`. Any
    adjacent connections that are already visited will not be traversed. The
    START cave will also not be visited. BIG caves can be visited more than
    once. Out of all small caves visited, only one of them can be visited at
    most twice. The rest of the small caves can be visited only at most once.''' 
    if cave.type is CaveType.END: return {(cave.name,)}

    paths = set()

    connection: Cave
    for connection in cave.connections:
        if connection in visited or connection.type is CaveType.START: continue

        new_first_small: Cave = first_small_cave
        if not new_first_small and connection.type is CaveType.SMALL:
            new_first_small = connection

        if first_small_cave and connection.type is CaveType.SMALL: visited.add(connection)
        connection_paths = _get_distinct_new_paths(connection, visited, new_first_small)
        if first_small_cave and connection.type is CaveType.SMALL: visited.remove(connection)

        if not first_small_cave:
            if connection.type is CaveType.SMALL: visited.add(connection)
            connection_paths |= _get_distinct_new_paths(connection, visited)
            if connection.type is CaveType.SMALL: visited.remove(connection)

        for path in connection_paths: paths.add((cave.name,) + path)

    return paths

def get_distinct_new_paths(cave_start: Cave) -> list:
    '''Returns a list of all distinct paths starting at `cave_start` to a cave of
    type 'CaveType.END' with new rules'''
    paths = _get_distinct_new_paths(cave_start)
    return paths

def main():
    connections = load_connections('input.txt')
    cave_start = build_cave(connections)
    paths = get_distinct_paths(cave_start)
    new_paths = get_distinct_new_paths(cave_start)

    print('Number of distinct paths:', len(paths))
    print('Number of distinct new paths:', len(new_paths))

if __name__ == '__main__':
    main()