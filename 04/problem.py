"""Advent of Code 2021 Problem 04 Code Solution."""

from typing import List, Tuple


def __check_win(board: List[List[int]], loc: Tuple[int, int]):
    """
    Return the win state of the board at `loc`.

    A win is determined if there is a row or column of Xs which contain `loc`.
    """
    row, col = loc
    win_horizontal, win_vertically = True, True
    for k in range(5):
        if board[row][k] != "X":
            win_horizontal = False
            break
    for k in range(5):
        if board[k][col] != "X":
            win_vertically = False
            break
    return win_horizontal or win_vertically


def __get_location(board: List[List[int]], value: int) -> tuple:
    """Return the location of `value` on `board`."""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == value:
                return (row, col)
    return None


def __mark_board(board: List[List[int]], loc: Tuple[int, int]) -> None:
    """Mark the `board` at `loc` with an 'X'."""
    row, col = loc
    board[row][col] = "X"


def __find_first_winning_board(
    boards: List[List[int]], drawings: List[int]
) -> Tuple[List[List[int]], int]:
    """Return the first winning board based on the `drawings` from `boards."""
    current_drawings = []
    for drawing in drawings:
        current_drawings.append(drawing)
        for board in boards:
            location = __get_location(board, drawing)
            if not location:
                continue
            __mark_board(board, location)
            if __check_win(board, location):
                return (board, current_drawings.pop())

    return (None, None)


def __find_last_winning_board(
    boards: List[List[int]], drawings: List[int]
) -> Tuple[List[List[int]], int]:
    """Return the last winning board based on the `drawings` from `boards."""
    current_drawings = []
    winning_board = None

    winning_draw: int
    winning_boards = []
    for drawing in drawings:
        current_drawings.append(drawing)
        for board in boards:
            if board in winning_boards:
                continue

            location = __get_location(board, drawing)
            if not location:
                continue

            __mark_board(board, location)
            if __check_win(board, location):
                winning_board, winning_draw = board, drawing
                winning_boards.append(board)

    return (winning_board, winning_draw)


def __get_sum_unmarked(board: List[List[int]]) -> int:
    """
    Return the sum of unmarked values on the `board`.

    Unmarked values are values that are not 'X'.
    """
    s = 0
    for row in board:
        for val in row:
            if val != "X":
                s += val
    return s


__drawings: list
__boards = []

with open("04/input.txt", "r") as f:
    __drawings = [int(x) for x in f.readline().split(",")]
    f.readline()

    board = []
    for line in f.readlines():
        line = line.strip()
        if line:
            vals = line.split(" ")
            board.append([int(x) for x in filter(lambda x: x, vals)])
        else:
            __boards.append(board)
            board = []


def part_one_answer() -> int:
    """Return the part one answer."""
    board, winning_number = __find_first_winning_board(__boards, __drawings)
    sum_unmarked = __get_sum_unmarked(board)
    return sum_unmarked * winning_number


def part_two_answer() -> int:
    """Return the part two answer."""
    board, winning_number = __find_last_winning_board(__boards, __drawings)
    sum_unmarked = __get_sum_unmarked(board)
    return sum_unmarked * winning_number
