"""Advent of Code 2021 Problem 17 Code Solution."""

from cmath import sqrt


def __p_x(step: int, v_x: int) -> int:
    """
    Return the x-position at step and v_x as the initial x velocity.

    This function is the closed form version of x as a parametric function.
    """
    c = v_x / abs(v_x) / 2
    if abs(v_x) <= step:
        step = v_x
    return int(-1 * pow(step, 2) * c + step * (v_x + c))


def __p_y(step: int, v_y: int) -> int:
    """
    Return the y-position at step and v_y as the initial y velocity.

    This function is the closed form version of y as a parametric function.
    """
    return int(step * (v_y - (step + 1) / 2 + 1))


def __get_bounds(filename: str) -> tuple[tuple[int], tuple[int]]:
    """Return the bounds of the target area specified in `filename`."""
    header = "target area: "
    with open(filename, "r") as f:
        line = f.readline()
        line = line[len(header) :]  # noqa E203
        x_info, y_info = line.split(", ")

        min_x, max_x = [
            int(x) for x in x_info[len("x=") :].split("..")  # noqa E203
        ]
        min_y, max_y = [
            int(y) for y in y_info[len("y=") :].split("..")  # noqa E203
        ]

    return ((min_x, max_x), (min_y, max_y))


def __get_valid_steps(v_y: int, y_dest: int) -> list[int]:
    """
    Return the valid steps using the __p_y quadratic equation.

    A valid step is defined as a real integer.
    """
    a = -0.5
    b = v_y + 0.5
    c = -y_dest
    d = pow(b, 2) - 4 * a * c
    t1: complex = (-b + sqrt(d)) / (2 * a)
    t2: complex = (-b - sqrt(d)) / (2 * a)

    def check(x: complex) -> int:
        """Return x as an integer if it is. Else, return None."""
        if x.imag != 0:
            return None
        else:
            x = x.real

        if x <= 0:
            return None

        if not x.is_integer():
            return None
        return x

    valid: list[int] = []

    t1 = check(t1)
    t2 = check(t2)

    if t1:
        valid.append(t1)
    if t2:
        valid.append(t2)

    return valid


def __get_all_initial_velocities(
    x_bounds: tuple[int], y_bounds: tuple[int]
) -> set[tuple[int, int]]:
    """Return list of all valid initial velocities that fall within bounds."""
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds

    velocities: set[tuple[int, int]] = set()

    for y_dest in range(y_min, y_max + 1):  # loop through all y destinations
        for v_y in range(
            y_dest, abs(y_dest)
        ):  # loop through possible initial y velocities
            valid_steps = __get_valid_steps(v_y, y_dest)
            if not valid_steps:
                continue

            for t in valid_steps:  # loop through all valid steps
                for v_x in range(
                    1, x_max + 1
                ):  # loop through all possible v_x
                    cur_x = __p_x(t, v_x)
                    if not x_min <= cur_x <= x_max:
                        continue
                    velocities.add((v_x, v_y))
    return velocities


def part_one_answer() -> int:
    """Return part one answer."""
    v_y = abs(__y_bounds[0]) - 1
    height = int((v_y) * (v_y + 1) / 2)
    return height


def part_two_answer() -> int:
    """Return part two answer."""
    velocities = sorted(__get_all_initial_velocities(__x_bounds, __y_bounds))
    return len(velocities)


__x_bounds, __y_bounds = __get_bounds("17/input.txt")
