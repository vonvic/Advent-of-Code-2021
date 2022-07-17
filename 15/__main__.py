from __future__ import annotations
from math import sqrt
from collections import namedtuple

Position = namedtuple('Position', ['x', 'y'])

class Matrix:
    def __init__(self, matrix: list[list[int]]):
        self._matrix = matrix
        self._marked = set()

    @property
    def row_count(self): return len(self._matrix)

    @property
    def col_count(self): return len(self._matrix[0])

    @property
    def rows(self): return self._matrix

    def at(self, position: Position):
        return self._matrix[position.y][position.x]
    
    def mark(self, position: Position):
        self._marked.add(position)

    def copy(self) -> Matrix:
        matrix_copy = []
        for row in self._matrix: matrix_copy.append(row.copy())
        return Matrix(matrix_copy)

    def increase_all(self, N):
        for i, row in enumerate(self._matrix):
            self._matrix[i] = [(x+N)%9 if (x+N)%9 != 0 else 9 for x in row]

    def __str__(self):
        s = ''

        for y, row in enumerate(self._matrix):
            for x, val in enumerate(row):
                s += str(val)
            s += '\n'
        return s[:-1]
    
    def __repr__(self): return str(self)

def get_map(filename: str) -> Matrix:
    '''Returns a matrix specified by matrix values in `filename`.'''
    matrix: list[list[int]] = []

    with open(filename, 'r') as f:
        for line in map(str.strip, f.readlines()):
            matrix.append([int(x) for x in line])

    return Matrix(matrix)

def get_full_map(original: Matrix) -> Matrix:
    '''Returns a matrix 5 times the size of `original`, where each values
    increase by matrix going down or right.'''
    new_matrix = []
    for _ in range(original.row_count*5):
        new_matrix.append([0 for _ in range(original.col_count*5)])

    for y, row in enumerate(original.rows):
        for x, val in enumerate(row):
            for i in range(5):
                for j in range(5):
                    curr_x = x+j*original.col_count
                    curr_y = y+i*original.row_count
                    new_val = (val+(i+j))%9 if (val+(i+j))%9 != 0 else 9
                    new_matrix[curr_y][curr_x] = new_val

    return Matrix(new_matrix)

def get_next_positions(matrix: Matrix, position: Position):
    '''Returns a collection of valid positions, where valid is a position that
    is not out of bounds of `matrix`'''
    positions = [
        Position(position.x, position.y-1),
        Position(position.x, position.y+1),
        Position(position.x-1, position.y),
        Position(position.x+1, position.y),
    ]
    valid_position = lambda p: p.x in range(matrix.col_count) and p.y in range(matrix.row_count)
    return filter(valid_position, positions)

def find_lowest_risk_path(matrix: Matrix):
    '''Returns the value of the lowest risk path by using the A* search
    algorithm.'''
    Node = namedtuple('Node', ['cost', 'position'])

    start = Position(x=0, y=0)
    goal = Position(x=matrix.col_count-1, y=matrix.row_count-1)

    def heuristic(p1: Position, p2: Position) -> float:
        return abs(p1.x-p1.y) + abs(p2.x-p2.y)

    def f(node: Node) -> float:
        return node.cost + heuristic(node.position, goal)
        # return node.cost

    # f = open('out.txt', 'r', 'f')

    current_node = Node(0, start)
    frontier = {current_node}
    discovered = {current_node.position}
    while frontier:
        best_node = min(frontier, key=f)
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
    return current_node.cost

def main():
    matrix = get_map('sample.txt')
    lowest_risk = find_lowest_risk_path(matrix)
    print('Value of lowest risk path:', lowest_risk)

    print('Generating full map...', end='')
    full_map = get_full_map(matrix)
    print('Complete!')

    lowest_risk = find_lowest_risk_path(full_map)
    print('Value of lowest risk path:', lowest_risk)

if __name__ == '__main__':
    main()