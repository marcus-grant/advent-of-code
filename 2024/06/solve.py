# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import numpy as np
from enum import Enum
import pathlib
import time
from typing import Union, List, Tuple, Set  # , Dict, Literal, NewType, Optional
from rich.console import Console
import sys

# Util imports
# from ..util.sols import cprint
console = Console()
cprint = console.print

# Solver ID Constants
DAY: str = "06"
TITLE: str = "Guard Gallivant"
COMMENTS: str = """Put any extra comments for helper script here"""

# Types
PathLike = Union[str, pathlib.Path]
Position = Tuple[int, int]
PositionSet = Set[Position]
PositionList = List[Position]


# Define cardinal direction enum
class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def parse_char_positions(lines: List[str], char: str = "#") -> PositionSet:
    """Parse the grid from the input lines.
    Not as a 2D array or list, but as a set of positions.
    The output is a set of tuples (row, col) for each '#' char in the grid.
    """
    grid = set()
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == char:
                grid.add((r, c))
    return grid


def parse_marker(lines: List[str]) -> Tuple[Position, Direction]:
    """Parse the marker position and direction from the input lines.
    The marker is the first '^', '>', 'v', or '<' character found in the grid.
    """
    markers = {"^": Direction.N, ">": Direction.E, "v": Direction.S, "<": Direction.W}
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch in markers:
                return (r, c), markers[ch]
    raise ValueError("No marker found in the grid.")


def cprint_grid(
    grid: PositionSet,
    marker: Position,
    dir: Direction,
    grid_len: int,
    width: int = 32,
    height: int = 32,
) -> None:
    """Prints a grid with obstacles from a PositionSet.
    Args:
        grid: A set of (row, col) tuples representing obstacles.
        width: Width of the grid.
        height: Height of the grid.
    """
    start_vert = max(marker[0] - height, 0)
    start_horz = max(marker[1] - width, 0)
    end_vert = min(marker[0] + height, grid_len)
    end_horz = min(marker[1] + width, grid_len)
    direction_markers = ["^", ">", "v", "<"]
    for r in range(start_vert, end_vert):
        for c in range(start_horz, end_horz):
            if (r, c) in grid:
                cprint("#", end="", style="red")
            elif (r, c) == marker:
                m = direction_markers[dir.value]
                cprint(m, end="", style="bold green")
            else:
                cprint(".", end="", style="color(8)")
        cprint("")


def inside_grid(pos: Position, grid_len: int) -> bool:
    if pos[0] < 0 or pos[1] < 0:
        return False
    if pos[0] >= grid_len or pos[1] >= grid_len:
        return False
    return True


def step_till_obstacle(
    pos_marker: Position, dir_marker: Direction, obstacles: PositionSet, grid_len: int
) -> Position:
    """Move the marker in the direction it's facing until it hits an obstacle.
    Returns the position where the marker stops.
    """
    while inside_grid(pos_marker, grid_len):
        # Move the marker in the direction it's facing
        if dir_marker == Direction.N:
            pos_marker = (pos_marker[0] - 1, pos_marker[1])
        elif dir_marker == Direction.E:
            pos_marker = (pos_marker[0], pos_marker[1] + 1)
        elif dir_marker == Direction.S:
            pos_marker = (pos_marker[0] + 1, pos_marker[1])
        elif dir_marker == Direction.W:
            pos_marker = (pos_marker[0], pos_marker[1] - 1)
        # If the marker hits an obstacle, stop
        if pos_marker in obstacles:
            break
    return pos_marker


def turn(dir_marker: Direction) -> Direction:
    """From given marker direction, return new direction enum turned right."""
    return Direction((dir_marker.value + 1) % 4)


def record_path(path: List[Position], pos_marker: Position) -> List[Position]:
    """Record the path taken by the marker. By looking at previously recorded positions."""
    if len(path) == 0:
        return [pos_marker]
    # If the marker is at the same position as the last recorded position, it's stuck
    if pos_marker == path[-1]:
        raise ValueError("Marker is stuck, infinite loop.")
    steps = 0
    stepped_vertically = False
    # Now we can record by checking direction of marker and last recorded position
    # Remember to check that the motion is only in one axis
    # First find out which axis the marker is moving in
    if pos_marker[0] == path[-1][0]:
        # Horizontal motion - Now make sure there's no vertical motion
        if pos_marker[1] != path[-1][1]:
            raise ValueError("Marker is moving in two axes, something's wrong.")
        steps = pos_marker[1] - path[-1][1]
        # Now add positions to the path in the direction of motion

    if pos_marker[1] == path[-1][1]:
        # Vertical motion - We already know there's no horizontal motion
        steps = pos_marker[0] - path[-1][0]
        stepped_vertically = True

    curr_pos = path[-1]
    while steps != 0:
        if stepped_vertically:
            curr_pos = (curr_pos[0] + 1, curr_pos[1])
        else:
            curr_pos = (curr_pos[0], curr_pos[1] + 1)
        path.append(pos_marker)
        if steps > 0:
            steps -= 1
        if steps < 0:
            steps += 1


def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # First parse grid positions as a set
    # It's a sparse grid, so it's more efficient storing obstacle positions
    pos_obstacles = parse_char_positions(lines)
    pos_marker, dir_marker = parse_marker(lines)
    grid_len = len(lines)

    if debug:
        cprint("Original Grid:")
        cprint(lines)
        cprint("Parsed Obstacle Positions:")
        cprint_grid(pos_obstacles, pos_marker, dir_marker, grid_len)

    # While the marker is within the grid, or a step max is reached...
    MAX_STEPS = 10**6
    steps = 0
    while inside_grid(pos_marker, grid_len) and steps < MAX_STEPS:
        # step till obstacle
        args = (pos_marker, dir_marker, pos_obstacles, grid_len)
        pos_marker = step_till_obstacle(*args)
        # Turn right
        dir_marker = turn(dir_marker)
        # If debug, print grid with marker and obstacles
        if debug:
            cprint(f"Step {steps}:")
            cprint_grid(pos_obstacles, pos_marker, dir_marker, grid_len)
        # NOTE: Very important to count steps to prevent infinite loops
        steps += 1

    return 69


def part2(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # TODO: Implement solution here

    return 420


def bgrn(s) -> str:
    return f"\033[1;32m{s}\033[0m"


def mgta(s) -> str:
    return f"\033[35m{s}\033[0m"


def blue(s) -> str:
    return f"\033[34m{s}\033[0m"


def run(debug: bool = False) -> None:
    """Runs the solution for both Part 1 and Part 2, prints results with timing.
    Args:
        debug: If True, runs in debug mode with verbose output.
    """
    PATH_EX = pathlib.Path(__file__).parent / "example.txt"
    PATH_IN = pathlib.Path(__file__).parent / "input.txt"
    kw = {"debug": debug}

    print(f"\n{mgta('Day')} {bgrn(DAY)} - {mgta(TITLE)}\n")
    print(f"\n{bgrn('Part 1')}:\n")

    tstart = time.time()
    sol = part1(PATH_EX, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Example Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))

    # tstart = time.time()
    # sol = part1(PATH_IN, **kw)
    # ms = f"{1000 * (time.time() - tstart):.3f}"
    # print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    # print(blue(f"Time taken (ms):\t\t{ms}\n"))

    # print(f"\n{bgrn('Part 2')}:\n")

    # tstart = time.time()
    # sol = part2(PATH_EX, **kw)
    # ms = f"{1000 * (time.time() - tstart):.3f}"
    # print(f"\n{mgta('Solution with Example Data:')}\t{bgrn(sol)}\n")
    # print(blue(f"Time taken (ms):\t\t{ms}\n"))

    # tstart = time.time()
    # sol = part2(PATH_IN, **kw)
    # ms = f"{1000 * (time.time() - tstart):.3f}"
    # print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    # print(blue(f"Time taken (ms):\t\t{ms}\n"))


if __name__ == "__main__":
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)

