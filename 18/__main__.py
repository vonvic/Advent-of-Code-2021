from __future__ import annotations
from ast import literal_eval
from asyncio import proactor_events
from math import ceil, floor
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
        self._left.parent = self
        self._right: Node = right
        self._right.parent = self
    
    @property
    def left(self) -> Node: return self._left

    @left.setter
    def left(self, value: Node):
        Node._check_value_type(value, Node)
        self._left = value
        self._left.parent = self

    @property
    def right(self) -> Node: return self._right

    @right.setter
    def right(self, value: Node):
        Node._check_value_type(value, Node)
        self._right = value
        self._right.parent = self

    def __str__(self) -> str:
        return f'[{self._left}, {self._right}]'

class ValueNode(Node):
    def __init__(self, parent: Node=None, prev_val: ValueNode=None,
                 next_val: ValueNode=None, value: int=None, depth: int=1):
        super().__init__(parent, depth)
        self._value: int = value
        self._prev: ValueNode = prev_val
        self._next: ValueNode = next_val

    @property
    def value(self) -> int: return self._value

    @value.setter
    def value(self, new_value: int):
        Node._check_value_type(new_value, int)
        self._value = new_value

    @property
    def prev(self) -> ValueNode: return self._prev

    @prev.setter
    def prev(self, value: ValueNode):
        Node._check_value_type(value, ValueNode)
        self._prev = value

    @property
    def next(self) -> ValueNode: return self._next

    @next.setter
    def next(self, value: ValueNode):
        Node._check_value_type(value, ValueNode)
        self._next = value

    def __str__(self) -> str: return str(self._value)

class LanternNumber:
    MAX_DEPTH: int = 4
    MAX_VALUE: int = 9

    def __init__(self, num_list: list = None):
        if num_list:
            self._root: ConnectingNode = self._build_tree(num_list)
            self._leaf_parents: list[ConnectingNode] = []
            self._leaves: list[ValueNode] = []
            self._gather_leaf_parents()
            self._reduce()
        else:
            self._root: ConnectingNode = None

    def _build_tree(self, num_list: list, depth=1) -> ConnectingNode:
        L, R = num_list
        L_node = self._build_tree(L, depth+1) if isinstance(L, list) else ValueNode(value=L, depth=depth+1)
        R_node = self._build_tree(R, depth+1) if isinstance(R, list) else ValueNode(value=R, depth=depth+1)

        connecting = ConnectingNode(left=L_node, right=R_node, depth=depth)
        connecting.left.parent = connecting
        connecting.right.parent = connecting
        return connecting

    def _rec_gather_leaves(self, node: Node) -> ValueNode:
        if isinstance(node, ValueNode):
            self._leaves.append(node)
        else:
            self._rec_gather_leaves(node.left)
            self._rec_gather_leaves(node.right)

    def _gather_leaf_parents(self):
        self._rec_gather_leaves(self._root)
        prev_leaf = self._leaves[0]
        for curr_leaf in self._leaves[1:]:
            prev_leaf.next = curr_leaf
            curr_leaf.prev = prev_leaf
            prev_leaf = curr_leaf

    def _reduce(self):
        while True:
            # print(self)
            node_to_explode = self._find_explode()
            if node_to_explode:
                # print('Explode!')
                self._explode(node_to_explode)
                continue

            node_to_split = self._find_split()
            if node_to_split:
                # print('Split!')
                self._split(node_to_split)
                continue

            break
    
    def _rec_find_explode(self, node: Node):
        if isinstance(node, ValueNode): return None

        if isinstance(node, ConnectingNode) and node.depth > LanternNumber.MAX_DEPTH:
            return node
        
        left = self._rec_find_explode(node.left)
        if left: return left

        right = self._rec_find_explode(node.right)
        if right: return right

        return None

    def _find_explode(self) -> ConnectingNode:
        return self._rec_find_explode(self._root)

    def _explode(self, node: ConnectingNode) -> None:
        prev_leaf: ValueNode = node.left.prev
        next_leaf: ValueNode = node.right.next

        if prev_leaf:
            prev_leaf.value += node.left.value
        if next_leaf:
            next_leaf.value += node.right.value

        parent: ConnectingNode = node.parent
        new_node = ValueNode(value=0, depth=node.depth)
        new_node.parent = parent

        if prev_leaf:
            prev_leaf.next = new_node
            new_node.prev = prev_leaf
        if next_leaf:
            new_node.next = next_leaf
            next_leaf.prev = new_node

        if parent.left is node:
            parent.left = new_node
        else:
            parent.right = new_node

    def _rec_find_split(self, node: Node) -> ValueNode:
        if isinstance(node, ValueNode):
            return node if node.value > LanternNumber.MAX_VALUE else None
        else:
            left = self._rec_find_split(node.left)
            if left: return left

            right = self._rec_find_split(node.right)
            if right: return right

            return None

    def _find_split(self) -> ValueNode:
        return self._rec_find_split(self._root)

    def _split(self, node: ValueNode) -> None:
        prev_leaf: ValueNode = node.prev
        next_leaf: ValueNode = node.next

        parent = node.parent

        left = ValueNode(value=floor(node.value/2), depth=node.depth+1)
        right = ValueNode(value=ceil(node.value/2), depth=node.depth+1)

        left.next = right
        right.prev = left

        if prev_leaf:
            prev_leaf.next = left
            left.prev = prev_leaf
        if next_leaf:
            right.next = next_leaf
            next_leaf.prev = right

        new_node = ConnectingNode(parent=parent, left=left, right=right, depth=node.depth)
        
        if parent.left is node:
            parent.left = new_node
        else:
            parent.right = new_node

    def __str__(self) -> str: return str(self._root)

    def __repr__(self): return self(self)

    def _increase_depth(self, node: Node):
        node.depth += 1
        if isinstance(node, ConnectingNode):
            self._increase_depth(node.left)
            self._increase_depth(node.right)

    def __add__(self, other: LanternNumber):
        lantern_sum = LanternNumber()

        curr = self._root
        while not isinstance(curr, ValueNode):
            curr = curr.right
        right_node = curr

        curr = other._root
        while not isinstance(curr, ValueNode):
            curr = curr.left
        left_node = curr

        right_node.next = left_node
        left_node.prev = right_node


        lantern_sum._root = ConnectingNode(depth=0, left=self._root, right=other._root)
        lantern_sum._increase_depth(lantern_sum._root)
        lantern_sum._reduce()
        return lantern_sum

def get_lantern_number_list(filename: str) -> list[LanternNumber]:
    lantern_numbers: list[LanternNumber] = []

    with open(filename, 'r') as f:
        for line in [x.rstrip() for x in f.readlines()]:
            lantern_numbers.append(LanternNumber(literal_eval(line)))

    return lantern_numbers

def main():
    lantern_numbers = get_lantern_number_list('18/sample_10.txt')

    # for lantern_number in lantern_numbers:
    #     print(lantern_number)
    
    print('Start!')
    prev = lantern_numbers[0]
    for curr in lantern_numbers[1:]:
        # print(f'{prev} + {curr}')
        prev = prev + curr
        print('Current Sum:', prev)

    print('Final:', prev)

if __name__ == '__main__':
    main()