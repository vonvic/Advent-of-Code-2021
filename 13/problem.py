"""Advent of Code 2021 Problem 13 Code Solution."""


def __get_points_and_folds(filename: str) -> tuple:
    """Return points and folds specified in file titled `filename`."""
    data: list

    with open(filename, "r") as f:
        data = [line.strip() for line in f.readlines()]

    sep = data.index("")

    points = []
    for line in data[:sep]:
        x, y = line.split(",")
        points.append((int(x), int(y)))

    folds = []
    for line in data[sep + 1 :]:  # noqa E203
        axis, position = line.split("=")
        axis = axis[-1]
        folds.append((axis, int(position)))

    return (points, folds)


def __get_matrix_size_from_points(points: list[tuple]) -> tuple:
    """Return the (x, y) size of matrix."""
    rows, cols = points[0]

    for x, y in points[1:]:
        cols = max(cols, x)
        rows = max(rows, y)

    return rows + 1, cols + 1


def __default_matrix(rows: int, cols: int) -> list:
    """Return a matrix of size (`rows`, `cols`) with each point being a '.'."""
    matrix = []
    for _ in range(rows):
        matrix.append(["." for _ in range(cols)])
    return matrix


def __matrix_str(matrix: list[list[str]]) -> str:
    """Return a string representation of `matrix`."""
    s = ""
    for row in matrix:
        s += "".join(row) + "\n"
    return s


def __plot_points(matrix: list[list[str]], points: list[tuple]):
    """Plot all points in `matrix` by assigning each value with `#`."""
    for x, y in points:
        matrix[y][x] = "#"


def __get_size_points_folds(filename: str) -> tuple:
    """Return the set of points and collection of folds defined in `filname`.

    The folds is a list of all the folds to be made in the form of (axis,
    position). The matrix will be filled with periods, and '#' in place of
    points specified in `filename`.
    """
    points, folds = __get_points_and_folds(filename)
    __get_matrix_size_from_points(points)
    return set(points), folds


def __get_reflection(point: tuple, fold: tuple):
    """Return the reflection of `point` at the line specifed at `fold`."""
    axis, position = fold
    x, y = point
    match axis:
        case "x":
            return (2 * position - x, y)
        case "y":
            return (x, 2 * position - y)
        case _:
            raise ValueError(f"Unknown axis: {axis}")


def __simulate_folding(points: list, folds: list):
    """
    Simulate folding of points defined by `folds` and return the points.

    The folding is defined by finding the reflection of a point only on one
    side.
    """
    points = set(points)

    for fold in folds:
        axis, position = fold
        new_points = set()  # gather new points after folding each point
        for point in points:
            x, y = point
            new_point: tuple = point
            match axis:
                case "x":
                    if x > position:
                        new_point = __get_reflection(point, fold)
                case "y":
                    if y > position:
                        new_point = __get_reflection(point, fold)
                case _:
                    raise ValueError(f"Unknown axis: {axis}")
            new_points.add(new_point)
        points = new_points
    return points


def part_one_answer() -> int:
    """Return part one answer."""
    new_points_first_fold = __simulate_folding(__points, __folds[:1])
    return len(new_points_first_fold)


def part_two_answer() -> str:
    """Return part two answer."""
    new_points = __simulate_folding(__points, __folds)
    rows, cols = __get_matrix_size_from_points(list(new_points))
    matrix = __default_matrix(rows, cols)
    __plot_points(matrix, new_points)
    return __matrix_str(matrix)


__points, __folds = __get_size_points_folds("13/input.txt")
