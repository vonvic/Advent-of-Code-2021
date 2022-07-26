from __future__ import annotations
from ast import literal_eval

class Node:
    def _check_value_type(value, expected_type) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(f'{value} is not of type {expected_type}')

    def __init__(self, parent: Node=None):
        self._parent: Node = parent
    
    @property
    def parent(self): return self._parent

    @parent.setter
    def parent(self, value: Node):
        Node._check_value_type(value, Node)
        self._parent = value

class ConnectingNode(Node):
    def __init__(self, parent: Node=None, left: Node=None, right: Node=None):
        super().__init__(parent)
        self._left: Node = left
        self._right: Node = right
    
    @property
    def left(self): return self._left

    @left.setter
    def left(self, value: Node):
        Node._check_value_type(value, Node)
        self._left = value

    @property
    def right(self): return self._right

    @right.setter
    def right(self, value: Node):
        Node._check_value_type(value, Node)
        self._right = value

    def __str__(self) -> str:
        return f'[{self._left}, {self._right}]'

class ValueNode(Node):
    def __init__(self, parent: Node=None, value: int=None):
        super().__init__(parent)
        self._value: int = value

    @property
    def value(self): return self._value

    @value.setter
    def value(self, new_value: int):
        Node._check_value_type(new_value, int)
        self._value = new_value

    def __str__(self) -> str: return str(self._value)

class LanternNumber:
    def _build_tree(num_list: list) -> ConnectingNode:
        L, R = num_list
        L_node = LanternNumber._build_tree(L) if isinstance(L, list) else ValueNode(value=L)
        R_node = LanternNumber._build_tree(R) if isinstance(R, list) is list else ValueNode(value=R)

        connecting = ConnectingNode(left=L_node, right=R_node)
        connecting.left.parent = connecting
        connecting.right.parent = connecting
        return connecting

    def __init__(self, num_list: list):
        self._root: ConnectingNode = LanternNumber._build_tree(num_list)

    def __str__(self) -> str: return str(self._root)

    def __repr__(self): return self(self)

def get_lantern_number_list(filename: str) -> list[LanternNumber]:
    lantern_numbers: list[LanternNumber] = []

    with open(filename, 'r') as f:
        for line in [x.rstrip() for x in f.readlines()]:
            lantern_numbers.append(LanternNumber(literal_eval(line)))

    return lantern_numbers

def main():
    lantern_numbers = get_lantern_number_list('test.txt')

    for lantern_number in lantern_numbers:
        print(lantern_number)

if __name__ == '__main__':
    main()