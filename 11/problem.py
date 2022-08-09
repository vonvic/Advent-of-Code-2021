"""Advent of Code 2021 Problem 11 Code Solution."""

RESET = "\u001b[0m"
BRIGHT_CYAN = "\u001b[36;1m"
CYAN = "\u001b[36m"
CLEAR_SCREEN = "\u001b[2J"


def print_energy_levels(energy_levels):
    """Display all energy levels to terminal, decorated with ASCII colors."""
    for row in energy_levels:
        for x in row:
            print(f"{CYAN if x > 0 else BRIGHT_CYAN}{x}", end=f"{RESET} ")
        print()


def increase_all(energy_levels):
    """Increase all energy levels by 1."""
    for row in range(len(energy_levels)):
        for col in range(len(energy_levels[row])):
            energy_levels[row][col] += 1


def flash(energy_levels, row, col):
    """Flash the octopus at (row, col)."""
    energy_level = energy_levels[row][col]
    if energy_level == 0:
        return 0
    if energy_level < 9:
        energy_levels[row][col] += 1
        return 0

    energy_levels[row][col] = 0

    ROW_N, COL_N = len(energy_levels), len(energy_levels[row])
    has_L, has_R = col > 0, col < COL_N - 1
    has_U, has_D = row > 0, row < ROW_N - 1
    # initialize with 1 to count itself
    flash_count = 1
    flash_count += flash(energy_levels, row, col - 1) if has_L else 0
    flash_count += (
        flash(energy_levels, row - 1, col - 1) if has_U and has_L else 0
    )
    flash_count += flash(energy_levels, row - 1, col) if has_U else 0
    flash_count += (
        flash(energy_levels, row - 1, col + 1) if has_U and has_R else 0
    )
    flash_count += flash(energy_levels, row, col + 1) if has_R else 0
    flash_count += (
        flash(energy_levels, row + 1, col + 1) if has_D and has_R else 0
    )
    flash_count += flash(energy_levels, row + 1, col) if has_D else 0
    flash_count += (
        flash(energy_levels, row + 1, col - 1) if has_D and has_L else 0
    )

    return flash_count


def init_flashes(energy_levels) -> int:
    """Initiate a flash for all energy levels that are at least 9."""
    flash_count = 0
    for row in range(len(energy_levels)):
        for col in range(len(energy_levels[row])):
            energy_level = energy_levels[row][col]
            could_flash = energy_level > 9

            if could_flash:
                flash_count += flash(energy_levels, row, col)
    return flash_count


def simulate(energy_levels: list, STEP_N: int, animate: bool = False) -> int:
    """
    Simulate the octopus flash behavior for `STEP_N` steps.

    Optionally, an animation can display in the terminal if `animate` is set to
    True.
    """
    from time import sleep

    flash_count = 0

    for _ in range(STEP_N):
        increase_all(energy_levels)
        num_of_flashes = init_flashes(energy_levels)
        flash_count += num_of_flashes

        if animate:
            print(CLEAR_SCREEN)
            print_energy_levels(energy_levels)
            sleep(1 / 16)

    return flash_count


def first_step_to_synchronize(
    energy_levels: list, STEP_N: int, animate: bool = False
) -> int:
    """
    Return the first step to synchronize all the octopi flash.

    Optionally, an animation can display in the terminal if `animate` is set to
    True.
    """
    from time import sleep

    step_count = 0

    ROW_N, COL_N = len(energy_levels), len(energy_levels[0])
    max_flashes = ROW_N * COL_N

    while True:
        increase_all(energy_levels)
        num_of_flashes = init_flashes(energy_levels)

        if animate:
            print(CLEAR_SCREEN)
            print_energy_levels(energy_levels)
            sleep(1 / 16)

        step_count += 1
        if num_of_flashes == max_flashes:
            break

    return step_count


def get_energy_levels_map(filename: str) -> list:
    """Return a map of all octopus energy levels defined in `filename`."""
    energy_levels = []

    with open(filename, "r") as f:
        for line in f.readlines():
            row = [int(x) for x in line.strip()]
            energy_levels.append(row)

    return energy_levels


def copy(mat: list) -> list:
    """Return a deep copy of `mat`."""
    return [row.copy() for row in mat]


def part_one_answer() -> int:
    """Return part one answer."""
    flash_count = simulate(copy(__energy_levels), __STEP_N)
    return flash_count


def part_two_answer() -> int:
    """Return part two answer."""
    first_step = first_step_to_synchronize(copy(__energy_levels), __STEP_N)
    return first_step


__STEP_N = 100
__energy_levels = get_energy_levels_map("11/input.txt")
