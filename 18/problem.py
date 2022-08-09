"""Advent of Code 2021 Problem 18 Code Solution."""

from __future__ import annotations

from ast import literal_eval
from math import ceil, floor


class _Node:
    def _check_value_type(value, expected_type) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(f"{value} is not of type {expected_type}")

    def __init__(self, parent: _Node = None, depth: int = 1):
        self._parent: _Node = parent
        self._depth = depth

    @property
    def parent(self) -> _Node:
        return self._parent

    @parent.setter
    def parent(self, value: _Node):
        _Node._check_value_type(value, _Node)
        self._parent = value

    @property
    def depth(self) -> int:
        return self._depth

    @depth.setter
    def depth(self, value):
        _Node._check_value_type(value, int)
        self._depth = value


class _ConnectingNode(_Node):
    def __init__(
        self,
        parent: _Node = None,
        left: _Node = None,
        right: _Node = None,
        depth: int = 1,
    ):
        super().__init__(parent, depth)
        self._left: _Node = left
        self._left.parent = self
        self._right: _Node = right
        self._right.parent = self

    @property
    def left(self) -> _Node:
        return self._left

    @left.setter
    def left(self, value: _Node):
        _Node._check_value_type(value, _Node)
        self._left = value
        self._left.parent = self

    @property
    def right(self) -> _Node:
        return self._right

    @right.setter
    def right(self, value: _Node):
        _Node._check_value_type(value, _Node)
        self._right = value
        self._right.parent = self

    def __str__(self) -> str:
        return f"[{self._left}, {self._right}]"


class _ValueNode(_Node):
    def __init__(
        self,
        parent: _Node = None,
        prev_val: _ValueNode = None,
        next_val: _ValueNode = None,
        value: int = None,
        depth: int = 1,
    ):
        super().__init__(parent, depth)
        self._value: int = value
        self._prev: _ValueNode = prev_val
        self._next: _ValueNode = next_val

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int):
        _Node._check_value_type(new_value, int)
        self._value = new_value

    @property
    def prev(self) -> _ValueNode:
        return self._prev

    @prev.setter
    def prev(self, value: _ValueNode):
        _Node._check_value_type(value, _ValueNode)
        self._prev = value

    @property
    def next(self) -> _ValueNode:
        return self._next

    @next.setter
    def next(self, value: _ValueNode):
        _Node._check_value_type(value, _ValueNode)
        self._next = value

    def __str__(self) -> str:
        return str(self._value)


class _LanternNumber:
    MAX_DEPTH: int = 4
    MAX_VALUE: int = 9

    def __init__(self, num_list: list = None):
        if num_list:
            self._root: _ConnectingNode = self._build_tree(num_list)
            self._leaf_parents: list[_ConnectingNode] = []
            self._leaves: list[_ValueNode] = []
            self._gather_leaf_parents()
            self._reduce()
        else:
            self._root: _ConnectingNode = None

    # def __deepcopy__(self)

    def _build_tree(self, num_list: list, depth=1) -> _ConnectingNode:
        L, R = num_list
        L_Node = (
            self._build_tree(L, depth + 1)
            if isinstance(L, list)
            else _ValueNode(value=L, depth=depth + 1)
        )
        R_Node = (
            self._build_tree(R, depth + 1)
            if isinstance(R, list)
            else _ValueNode(value=R, depth=depth + 1)
        )

        connecting = _ConnectingNode(left=L_Node, right=R_Node, depth=depth)
        connecting.left.parent = connecting
        connecting.right.parent = connecting
        return connecting

    def _rec_gather_leaves(self, node: _Node) -> _ValueNode:
        if isinstance(node, _ValueNode):
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

    def _find_explode(self) -> _ConnectingNode:
        curr = self._root
        while not isinstance(curr, _ValueNode):
            curr = curr.left

        def violates_depth(node: _Node):
            """Determine if node's depth is out of range."""
            return node.depth > _LanternNumber.MAX_DEPTH

        while curr and not violates_depth(curr.parent):
            curr = curr.next

        return curr.parent if curr else None

    def _explode(self, node: _ConnectingNode) -> None:
        prev_leaf: _ValueNode = node.left.prev
        next_leaf: _ValueNode = node.right.next

        if prev_leaf:
            prev_leaf.value += node.left.value
        if next_leaf:
            next_leaf.value += node.right.value

        parent: _ConnectingNode = node.parent
        new_Node = _ValueNode(value=0, depth=node.depth)
        new_Node.parent = parent

        if prev_leaf:
            prev_leaf.next = new_Node
            new_Node.prev = prev_leaf
        if next_leaf:
            new_Node.next = next_leaf
            next_leaf.prev = new_Node

        if parent.left is node:
            parent.left = new_Node
        else:
            parent.right = new_Node

    def _find_split(self) -> _ValueNode:
        curr = self._root
        while not isinstance(curr, _ValueNode):
            curr = curr.left

        def violates_value(node: _Node) -> bool:
            """Determine if node is out of range."""
            return node.value > _LanternNumber.MAX_VALUE

        while curr and not violates_value(curr):
            curr = curr.next

        return curr

    def _split(self, node: _ValueNode) -> None:
        prev_leaf: _ValueNode = node.prev
        next_leaf: _ValueNode = node.next

        parent = node.parent

        left = _ValueNode(value=floor(node.value / 2), depth=node.depth + 1)
        right = _ValueNode(value=ceil(node.value / 2), depth=node.depth + 1)

        left.next = right
        right.prev = left

        if prev_leaf:
            prev_leaf.next = left
            left.prev = prev_leaf
        if next_leaf:
            right.next = next_leaf
            next_leaf.prev = right

        new_Node = _ConnectingNode(
            parent=parent, left=left, right=right, depth=node.depth
        )

        if parent.left is node:
            parent.left = new_Node
        else:
            parent.right = new_Node

    def __str__(self) -> str:
        return str(self._root)

    def __repr__(self):
        return self(self)

    def _increase_depth(self, node: _Node):
        node.depth += 1
        if isinstance(node, _ConnectingNode):
            self._increase_depth(node.left)
            self._increase_depth(node.right)

    def __add__(self, other: _LanternNumber):
        left, right = str(self), str(other)
        together = literal_eval(f"[{left},{right}]")
        return _LanternNumber(together)

    def _magnitude(node: _Node) -> int:
        if isinstance(node, _ValueNode):
            return node.value
        if isinstance(node, _ConnectingNode):
            left_value = _LanternNumber._magnitude(node.left)
            right_value = _LanternNumber._magnitude(node.right)
            return 3 * left_value + 2 * right_value

    @property
    def magnitude(self) -> int:
        return _LanternNumber._magnitude(self._root)


def __get_lantern_number_list(filename: str) -> list[_LanternNumber]:
    """
    Return a list of lantern numbers defined in `filename`.

    Each line in `filename` is a lantern number. It'll be parsed when inputted
    in the constructor of a _LanternNumber object.
    """
    lantern_numbers: list[_LanternNumber] = []

    with open(filename, "r") as f:
        for line in [x.rstrip() for x in f.readlines()]:
            lantern_numbers.append(_LanternNumber(literal_eval(line)))

    return lantern_numbers


def part_one_answer() -> int:
    """Return part one answer."""
    curr_sum = __lantern_numbers[0]
    for curr in __lantern_numbers[1:]:
        curr_sum = curr_sum + curr
    return curr_sum.magnitude


def part_two_answer() -> int:
    """Return part two answer."""
    magnitudes = set()
    for this in __lantern_numbers:
        for other in __lantern_numbers:
            if this is other:
                continue
            magnitudes.add((this + other).magnitude)
    return max(magnitudes)


__lantern_numbers = __get_lantern_number_list("18/input.txt")
