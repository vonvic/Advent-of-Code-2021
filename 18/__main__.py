from __future__ import annotations
from ast import literal_eval

from numpy import isin
class Node:
    def _check_value_type(value, expected_type) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(f'{value} is not of type {expected_type}')

    def __init__(self, parent: Node=None, depth: int=1):
        self._parent: Node = parent
        self._depth = depth
    
    @property
    def parent(self) -> Node: return self._parent

    @parent.setter
    def parent(self, value: Node):
        Node._check_value_type(value, Node)
        self._parent = value

    @property
    def depth(self) -> int: return self._depth

    @depth.setter
    def depth(self, value):
        Node._check_value_type(value, int)
        self._depth = value

class ConnectingNode(Node):
    def __init__(self, parent: Node=None, left: Node=None, right: Node=None, depth: int=1):
        super().__init__(parent, depth)
        self._left: Node = left
        self._right: Node = right
    
    @property
    def left(self) -> Node: return self._left

    @left.setter
    def left(self, value: Node):
        Node._check_value_type(value, Node)
        self._left = value

    @property
    def right(self) -> Node: return self._right

    @right.setter
    def right(self, value: Node):
        Node._check_value_type(value, Node)
        self._right = value

    def __str__(self) -> str:
        return f'[{self._left}, {self._right}]'

class ValueNode(Node):
    def __init__(self, parent: Node=None, value: int=None, depth: int=1):
        super().__init__(parent, depth)
        self._value: int = value

    @property
    def value(self) -> int: return self._value

    @value.setter
    def value(self, new_value: int):
        Node._check_value_type(new_value, int)
        self._value = new_value

    def __str__(self) -> str: return str(self._value)

class LanternNumber:
    MAX_DEPTH: int = 4

    def __init__(self, num_list: list):
        self._root: ConnectingNode = self._build_tree(num_list)
        self._leaf_parents: list[ConnectingNode] = []
        self._gather_leaf_parents()
        self._reduce()

    def _build_tree(self, num_list: list, depth=1) -> ConnectingNode:
        L, R = num_list
        L_node = self._build_tree(L, depth+1) if isinstance(L, list) else ValueNode(value=L)
        R_node = self._build_tree(R, depth+1) if isinstance(R, list) else ValueNode(value=R)

        connecting = ConnectingNode(left=L_node, right=R_node, depth=depth)
        connecting.left.parent = connecting
        connecting.right.parent = connecting
        return connecting

    def _rec_gather_leaf_parents(self, node: Node):
        if isinstance(node, ValueNode): return

        self._rec_gather_leaf_parents(node.left)
        if isinstance(node.left, ValueNode) or isinstance(node.right, ValueNode):
            self._leaf_parents.append(node)
        self._rec_gather_leaf_parents(node.right)

    def _gather_leaf_parents(self):
        self._rec_gather_leaf_parents(self._root)

    def _reduce(self):
        new_leaf_parents: list[ConnectingNode] = []
        for index, node in enumerate(self._leaf_parents):
            violates_depth = node.depth > LanternNumber.MAX_DEPTH
            new_leaf_parent = self._explode(index, node) if violates_depth else node
            new_leaf_parents.append(new_leaf_parent)
        self._leaf_parents = new_leaf_parents

    def _explode(self, index: int, node: ConnectingNode):
        if index > 0:
            left_parent = self._leaf_parents[index-1]
            if isinstance(left_parent.right, ValueNode):
                left_parent.right.value += node.left.value
            else:
                left_parent.left.value += node.left.value

        if index < len(self._leaf_parents)-1:
            right_parent = self._leaf_parents[index+1]
            if isinstance(right_parent.left, ValueNode):
                right_parent.left.value += node.right.value
            else:
                right_parent.right.value += node.right.value

        parent: ConnectingNode = node.parent
        new_node = ValueNode(value=0)
        new_node.parent = parent

        if parent.left is node:
            parent.left = new_node
        else:
            parent.right = new_node

        return parent

    def _split(node: ValueNode):
        pass

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