# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import numpy as np
from enum import Enum
import pathlib
import time
from typing import Union, List, Tuple, Set
from rich.console import Console
import sys

console = Console()
cprint = console.print

DAY: str = "06"
TITLE: str = "Guard Gallivant"
COMMENTS: str = """Put any extra comments for helper script here"""

# Types
PathLike = Union[str, pathlib.Path]
Position = Tuple[int, int]
PositionSet = Set[Position]
PositionList = List[Position]


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
    """Parse positions of obstacles '#' from the input lines."""
    grid = set()
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == char:
                grid.add((r, c))
    return grid


def parse_marker(lines: List[str]) -> Tuple[Position, Direction]:
    """Parse the guard's starting position and direction from markers: '^', '>', 'v', '<'."""
    markers = {"^": Direction.N, ">": Direction.E, "v": Direction.S, "<": Direction.W}
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch in markers:
                return (r, c), markers[ch]
    raise ValueError("No marker found in the grid.")


def inside_grid(pos: Position, grid_len: int) -> bool:
    """Check if position is inside the square grid."""
    return 0 <= pos[0] < grid_len and 0 <= pos[1] < grid_len


def turn(dir_marker: Direction) -> Direction:
    """Turn direction 90 degrees to the right."""
    return Direction((dir_marker.value + 1) % 4)


def forward_pos(pos: Position, dir_marker: Direction) -> Position:
    """Get the forward position in the direction the guard is facing."""
    if dir_marker == Direction.N:
        return (pos[0] - 1, pos[1])
    elif dir_marker == Direction.E:
        return (pos[0], pos[1] + 1)
    elif dir_marker == Direction.S:
        return (pos[0] + 1, pos[1])
    elif dir_marker == Direction.W:
        return (pos[0], pos[1] - 1)


def record_path(path: List[Position], pos_marker: Position) -> List[Position]:
    """Record intermediate positions between last recorded and the new pos_marker.

    We assume motion is either purely horizontal or purely vertical.
    If both row and column changed, raise an error.
    """
    if len(path) == 0:
        path.append(pos_marker)
        return path

    last = path[-1]
    drow = pos_marker[0] - last[0]
    dcol = pos_marker[1] - last[1]

    # If no movement
    if drow == 0 and dcol == 0:
        # no movement, just return
        return path

    # If both row and column changed, it's invalid
    if drow != 0 and dcol != 0:
        raise ValueError("Marker moved diagonally, which should not happen.")

    if drow != 0:
        # vertical movement
        step = 1 if drow > 0 else -1
        for _ in range(abs(drow)):
            curr = path[-1]
            new_pos = (curr[0] + step, curr[1])
            path.append(new_pos)
    elif dcol != 0:
        # horizontal movement
        step = 1 if dcol > 0 else -1
        for _ in range(abs(dcol)):
            curr = path[-1]
            new_pos = (curr[0], curr[1] + step)
            path.append(new_pos)

    return path


def cprint_grid(
    grid: PositionSet,
    marker: Position,
    dir: Direction,
    grid_len: int,
    visited: PositionSet,
    width: int = 32,
    height: int = 32,
) -> None:
    """Prints a portion of the grid around the marker.
    Obstacles: '#', red
    Marker: direction symbol in bold green
    Visited (except current marker): '.' in yellow
    Unvisited empty: '.' in dim gray
    """
    start_vert = max(marker[0] - height, 0)
    start_horz = max(marker[1] - width, 0)
    end_vert = min(marker[0] + height, grid_len)
    end_horz = min(marker[1] + width, grid_len)
    direction_markers = ["^", ">", "v", "<"]

    for r in range(start_vert, end_vert):
        line_chars = []
        for c in range(start_horz, end_horz):
            if (r, c) in grid:
                line_chars.append(("#", "red"))
            elif (r, c) == marker:
                m = direction_markers[dir.value]
                line_chars.append((m, "bold green"))
            else:
                if (r, c) in visited:
                    line_chars.append(("x", "color(8)"))
                else:
                    line_chars.append((".", "color(8)"))
        # Print line
        for ch, style in line_chars:
            cprint(ch, end="", style=style)
        cprint("")  # new line


def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)
    pos_obstacles = parse_char_positions(lines)
    pos_marker, dir_marker = parse_marker(lines)
    grid_len = len(lines)

    visited = set()
    visited.add(pos_marker)

    MAX_STEPS = 10**6
    steps = 0

    while inside_grid(pos_marker, grid_len) and steps < MAX_STEPS:
        next_pos = forward_pos(pos_marker, dir_marker)

        if inside_grid(next_pos, grid_len):
            if next_pos in pos_obstacles:
                # Obstacle ahead, turn right
                dir_marker = turn(dir_marker)
                if debug:
                    cprint(f"[DEBUG] Step {steps}: Hit obstacle. Turned right.")
                    cprint_grid(
                        pos_obstacles, pos_marker, dir_marker, grid_len, visited
                    )
            else:
                # Move forward
                pos_marker = next_pos
                visited.add(pos_marker)
        else:
            # Stepping out of the grid
            pos_marker = next_pos
            break

        steps += 1

    return len(visited)


def part2(fpath: PathLike, debug: bool = False) -> int:
    # This is a placeholder for part 2
    # Currently returns a dummy value
    return 420


def bgrn(s) -> str:
    return f"\033[1;32m{s}\033[0m"


def mgta(s) -> str:
    return f"\033[35m{s}\033[0m"


def blue(s) -> str:
    return f"\033[34m{s}\033[0m"


def run(debug: bool = False) -> None:
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

    # Uncomment these lines if you have the real input.txt
    tstart = time.time()
    sol = part1(PATH_IN, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))

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
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)
