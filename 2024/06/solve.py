# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import numpy as np
from concurrent.futures import ProcessPoolExecutor
from enum import Enum
import os
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


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


class Grid:
    def __init__(self, lines: List[str], print_size: Position = (32, 64)):
        self.lines = lines
        self.print_height = print_size[0]
        self.print_width = print_size[1]
        self.grid_height = len(lines)
        self.grid_width = len(lines[0])
        self.pos_obstacles = self._parse_char_positions(lines)

        # Ensure all lines have the same width
        if not all(len(line) == self.grid_width for line in lines):
            raise ValueError("All lines should have the same width.")

    def _parse_char_positions(self, lines: List[str], char: str = "#") -> PositionSet:
        """Parse positions of obstacles '#' from the input lines."""
        grid = set()
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch == char:
                    grid.add((r, c))
        return grid

    def inside(self, pos: Position) -> bool:
        """Check if position is inside the grid."""
        if not (0 <= pos[0] < self.grid_height):
            return False
        if not (0 <= pos[1] < self.grid_width):
            return False
        return True

    def cprint(
        self,
        # DELETEME: old marker position and direction
        # marker: Position,
        # dir: Direction,
        guard: "Guard",
        visited: PositionSet,
    ) -> None:
        """Prints a portion of the grid around the marker.
        Obstacles: '#', red
        Marker: direction symbol in bold green
        Visited (except current marker): '.' in yellow
        Unvisited empty: '.' in dim gray
        """
        marker = guard.position
        dir = guard.direction
        start_vert = max(marker[0] - self.print_height, 0)
        start_horz = max(marker[1] - self.print_width, 0)
        end_vert = min(marker[0] + self.print_height, self.grid_height)
        end_horz = min(marker[1] + self.print_width, self.grid_width)
        direction_markers = ["^", ">", "v", "<"]

        for r in range(start_vert, end_vert):
            line_chars = []
            for c in range(start_horz, end_horz):
                if (r, c) in self.pos_obstacles:
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


class Guard:
    def __init__(self, position: Position, direction: Direction):
        self.position = position
        self.direction = direction

    @classmethod
    def _parse_marker(cls, lines: List[str]) -> Tuple[Position, Direction]:
        """Parse the guard's starting position and
        direction from markers: '^', '>', 'v', '<'.
        Return one of Direction enums and raise error if not found."""
        n, e, s, w = Direction.N, Direction.E, Direction.S, Direction.W
        markers = {"^": n, ">": e, "v": s, "<": w}
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch in markers:
                    return (r, c), markers[ch]
        raise ValueError("No marker found in the grid.")

    def turn(self) -> None:
        """Turn direction 90 degrees to the right."""
        self.direction = Direction((self.direction.value + 1) % 4)

    def forward_pos(self) -> Position:
        if self.direction == Direction.N:
            return (self.position[0] - 1, self.position[1])
        elif self.direction == Direction.E:
            return (self.position[0], self.position[1] + 1)
        elif self.direction == Direction.S:
            return (self.position[0] + 1, self.position[1])
        elif self.direction == Direction.W:
            return (self.position[0], self.position[1] - 1)
        else:
            raise ValueError("Invalid direction.")

    def move_forward(self):
        self.position = self.forward_pos()


# FIXME: The windowing logic is broken and print shape is inconsistent
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


def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)
    grid = Grid(lines)
    guard_start_pos, guard_start_dir = Guard._parse_marker(lines)
    guard = Guard(guard_start_pos, guard_start_dir)

    visited = set()
    visited.add(guard.position)

    MAX_STEPS = 10**6
    steps = 0

    while grid.inside(guard.position) and steps < MAX_STEPS:
        next_pos = guard.forward_pos()

        if grid.inside(next_pos):
            if next_pos in grid.pos_obstacles:
                # Obstacle ahead, turn right
                guard.turn()
                if debug:
                    cprint(f"[DEBUG] Step {steps}: Hit obstacle. Turned right.")
                    grid.cprint(guard, visited)
            else:
                # Move forward
                guard.move_forward()
                visited.add(guard.position)
        else:
            # Stepping out of the grid
            guard.position = next_pos
            break

        steps += 1

    return len(visited)


class Simulator:
    def __init__(self, grid: Grid, guard: Guard, max_steps: int = 10**6) -> None:
        self.grid = grid
        self.guard = guard
        self.MAX_STEPS = max_steps
        self.states = set()

    def run(self) -> bool:
        """Runs a simulation untill the guard leaves the grid or a loop is detected."""
        # Record init state
        self.states.add((self.guard.position, self.guard.direction))

        steps = 0
        while self.grid.inside(self.guard.position) and steps < self.MAX_STEPS:
            next_pos = self.guard.forward_pos()

            if self.grid.inside(next_pos):
                if next_pos in self.grid.pos_obstacles:
                    self.guard.turn()  # Obstacle ahead, turn right
                else:  # Move forward
                    self.guard.move_forward()
            else:  # Guard leaves grid, no loop found, end simulation
                return False

            steps += 1

            current_state = (self.guard.position, self.guard.direction)
            if current_state in self.states:
                return True  # Loop detected
            else:
                # Record state to check for a loop in the future
                self.states.add(current_state)

        # If we exit the loop normally, no loop was detected
        return False


def test_candidate(
    candidate: Position,
    grid: Grid,
    guard_pos: Position,
    guard_dir: Direction,
    max_steps: int = 10**6,
) -> bool:
    """
    Test if placing an obstruction at 'candidate' leads to a loop.
    - Adds the candidate obstruction to the grid.
    - Creates a new Guard from the input lines.
    - Runs the Simulator with the given grid and guard.
    - Removes the obstruction afterward.
    Returns True if a loop is detected, False otherwise.
    """
    # Place the obstruction
    grid.pos_obstacles.add(candidate)

    # Create new guard
    guard = Guard(guard_pos, guard_dir)

    # Run simulation
    sim = Simulator(grid, guard, max_steps=max_steps)
    loop_found = sim.run()

    # Remove the obstruction
    grid.pos_obstacles.remove(candidate)

    return loop_found


# NOTE: Before changing the code, the simulator took:
# 113555.607 ms
# NOTE: Before changing Guard to not parse lines every time it took
# 110783.375 ms
# NOTE: After implementing the candidate test with multiprocessing w/ 4 workers took:
# 54352.520 ms (2.04x speedup)
# Move run_candidate to top-level
def run_candidate(args: Tuple[Position, List[str], Position, Direction]) -> bool:
    candidate, lines, guard_start_pos, guard_start_dir = args
    test_grid = Grid(lines)
    return test_candidate(candidate, test_grid, guard_start_pos, guard_start_dir)


def part2(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)
    grid = Grid(lines)
    guard_start_pos, guard_start_dir = Guard._parse_marker(lines)

    # Generate candidates
    candidates = [
        (r, c)
        for r in range(grid.grid_height)
        for c in range(grid.grid_width)
        if (r, c) not in grid.pos_obstacles and (r, c) != guard_start_pos
    ]

    loop_count = 0

    # Prepare arguments for each candidate
    # We'll pass all needed data as a tuple so run_candidate can be pickled
    tasks = [
        (candidate, lines, guard_start_pos, guard_start_dir) for candidate in candidates
    ]

    # Adjust workers as you like (e.g. max_workers=4)
    with ProcessPoolExecutor(max_workers=4) as executor:
        for result in executor.map(run_candidate, tasks):
            if result:
                loop_count += 1

    return loop_count


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

    print(f"\n{bgrn('Part 2')}:\n")

    tstart = time.time()
    sol = part2(PATH_EX, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Example Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))

    tstart = time.time()
    sol = part2(PATH_IN, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))


if __name__ == "__main__":
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)
