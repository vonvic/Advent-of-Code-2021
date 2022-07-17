import enum
from math import sqrt
from tokenize import Name
from typing import NewType, NamedTuple
from collections import namedtuple
from unicodedata import name

RESET = '\u001b[0m'
WHITE = '\u001b[37m'
BRIGHT_WHITE = '\u001b[37;1m'
RED = '\u001b[31m'
CLEAR_CONSOLE = '\u001b[2J'

Position = namedtuple('Position', ['x', 'y'])

class Matrix:
    def __init__(self, matrix: list[list[int]]):
        self._matrix = matrix
        self._marked = set()

    @property
    def row_count(self): return len(self._matrix)

    @property
    def col_count(self): return len(self._matrix[0])

    def at(self, position: Position):
        return self._matrix[position.y][position.x]
    
    def mark(self, position: Position):
        self._marked.add(position)

    def __str__(self):
        s = ''

        for y, row in enumerate(self._matrix):
            for x, val in enumerate(row):
                pos = Position(x, y)
                color = RED if pos in self._marked else WHITE
                s += f'{color}{self.at(pos)}{RESET}'
            s += '\n'
        return s[:-1]
    
    def __repr__(self): return str(self)

def get_matrix(filename: str) -> Matrix:
    matrix: list[list[int]] = []

    with open(filename, 'r') as f:
        for line in map(str.strip, f.readlines()):
            matrix.append([int(x) for x in line])

    return Matrix(matrix)

def get_next_positions(matrix: Matrix, position: Position):
    from typing import Callable
    positions = [
        Position(position.x, position.y-1),
        Position(position.x, position.y+1),
        Position(position.x-1, position.y),
        Position(position.x+1, position.y),
    ]
    valid_position: Callable[[Position], None] = lambda p: p.x in range(matrix.col_count) and p.y in range(matrix.row_count)
    return filter(valid_position, positions)

def find_lowest_risk_path(matrix: Matrix):
    from time import sleep
    Node = namedtuple('Node', ['cost', 'position'])

    start = Position(x=0, y=0)
    goal = Position(x=matrix.col_count-1, y=matrix.row_count-1)

    def euclidean_distance(p1: Position, p2: Position) -> float:
        return sqrt(sum(map(lambda p: pow(p.x-p.y, 2), (p1, p2))))

    def f(node: Node) -> float:
        # return node.cost + euclidean_distance(node.position, goal)
        return node.cost

    current_node = Node(0, start)
    frontier = {current_node}
    discovered = {node.position for node in frontier | {current_node}}
    while frontier:
        best_node = min(frontier, key=f)
        # matrix.mark(best_node.position)
        # print(CLEAR_CONSOLE)
        # print(best_node, f(best_node))
        # print(matrix)
        frontier.remove(best_node)
        if best_node.position == goal:
            current_node = best_node
            break
        
        for position in get_next_positions(matrix, best_node.position):
            if position not in discovered:
                new_cost = best_node.cost + matrix.at(position)
                new_node = Node(new_cost, position)
                frontier.add(new_node)
                discovered.add(position)

        current_node = best_node
        # for node in sorted(frontier, key=lambda node: node.cost): print(node)
        # sleep(1)
        # print()
    print(current_node)
    return current_node.cost


def main():
    matrix = get_matrix('input.txt')
    lowest_risk = find_lowest_risk_path(matrix)
    print('Value of lowest risk path:', lowest_risk)

if __name__ == '__main__':
    main()