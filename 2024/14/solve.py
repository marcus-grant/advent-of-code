from collections import Counter
import pathlib
import re
import time
from typing import Union, List, Tuple
import sys

# Solver ID Constants
DAY: str = "14"
TITLE: str = "Restroom Redoubt"
COMMENTS: str = """
REALLY interesting one.
Using some of my templates for Grid & Position classes really sped things up.
The end result involves interesting analysis in ./analysis.py.
Essentially instead of sitting waiting for part2 to iterate 7286 times,
I used the analysis script to find when the quadrants have a lowest product.
What that means is that each quadrant holds the robots in the most compact form.
That tells us when the image forms.
It finds that 7286 iterations are needed to do it.
So I go back to the solver and input that number minus margin show the image.
"""

# Types
PathLike = Union[str, pathlib.Path]


class Position:
    def __init__(self, x: int, y: int):
        self.x: int = x  # Rightward increase (column iterator)
        self.y: int = y  # Downward increase (row iterator)

    def __add__(self, other: "Position"):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Velocity:
    def __init__(self, dx: int, dy: int):
        self.dx: int = dx  # Rightward increase (column iterator)
        self.dy: int = dy  # Downward increase (row iterator)

    def __mul__(self, scalar: int):
        return Position(self.dx * scalar, self.dy * scalar)

    def __hash__(self):
        return hash((self.dx, self.dy))

    def __repr__(self):
        return f"({self.dx}, {self.dy})"


class Robot:
    def __init__(self, line: str):
        parsed = self.parse_string(line)
        self.pos = parsed[0]
        self.vel = parsed[1]

    @staticmethod
    def parse_string(line: str) -> Tuple[Position, Velocity]:
        # Every robot spec line is of form: "p=<x,y> v=<dx,dy>"
        match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
        if match is None:
            raise ValueError(f"Invalid robot spec line: {line}")
        return (
            Position(int(match.group(1)), int(match.group(2))),
            Velocity(int(match.group(3)), int(match.group(4))),
        )

    def move(self, time: int = 1):
        self.pos = self.pos + (self.vel * time)

    def teleport(self, width: int, depth: int):
        self.pos.x = (self.pos.x + width) % width
        self.pos.y = (self.pos.y + depth) % depth

    def __hash__(self):
        return hash((self.pos, self.vel))

    def __repr__(self):
        return f"Robot(pos={self.pos}, vel={self.vel})"


class Grid:
    def __init__(self, fp: PathLike, width: int, height: int):
        lines = self.read_lines(fp)
        self.robots = [Robot(line) for line in lines]
        self.width = width
        self.height = height

    @staticmethod
    def read_lines(fpath: PathLike) -> List[str]:
        with open(fpath, "r") as f:
            lines = f.read().splitlines()
        return lines

    def move_robots(self, time: int = 1):
        for robot in self.robots:
            robot.move(time)
            robot.teleport(self.width, self.height)

    def print(self):
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        robot_pos_count = Counter(robot.pos for robot in self.robots)

        for pos, count in robot_pos_count.items():
            grid[pos.y][pos.x] = str(count) if count > 0 else "."

        for row in grid:
            print("".join(row))

    def calculate_safety_factor(self) -> int:
        mid_x = self.width // 2
        mid_y = self.height // 2

        quadrants = [0, 0, 0, 0]  # NW, NE, SW, SE

        for robot in self.robots:
            x, y = robot.pos.x, robot.pos.y

            if x == mid_x or y == mid_y:  # Skip boundary robots
                continue

            if x < mid_x and y < mid_y:
                quadrants[0] += 1  # NW
            elif x >= mid_x and y < mid_y:
                quadrants[1] += 1  # NE
            elif x < mid_x and y >= mid_y:
                quadrants[2] += 1  # SW
            else:
                quadrants[3] += 1  # SE

        # Multiply the number of robots in all quadrants
        safety_factor = 1
        for count in quadrants:
            safety_factor *= count
        return safety_factor


def part1(fpath: PathLike, debug: bool = False) -> int:
    if "example" in str(fpath):
        grid = Grid(fpath, 11, 7)
    else:
        grid = Grid(fpath, 101, 103)

    if debug:
        print("\nParsed robots:")
        for robot in grid.robots:
            print(robot)

    # Move the robots for 100s
    grid.move_robots(100)

    if debug:
        print("\nMoved robots:")
        for robot in grid.robots:
            print(robot)
        print("\nGrid state after 100 seconds:")
        grid.print()

    # Calculate and return the safety factor
    return grid.calculate_safety_factor()


def part2(fpath: PathLike, debug: bool = False) -> int:
    if "example" in str(fpath):
        grid = Grid(fpath, 11, 7)
    else:
        grid = Grid(fpath, 101, 103)

    iterations = 7280
    sleeptime = 0.4
    grid.move_robots(iterations)

    if debug:
        try:
            while iterations < 7286:
                grid.move_robots(1)
                grid.print()
                iterations += 1
                time.sleep(sleeptime)
                print(f"Iterations: {iterations}")
                print("\nCurrent grid state:")
                grid.print()

        except KeyboardInterrupt:
            print("\nInterrupted by user.")

    if debug:
        return iterations
    return 7286


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

    tstart = time.time()
    sol = part1(PATH_IN, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))

    print(f"\n{bgrn('Part 2')}:\n")

    tstart = time.time()
    sol = part2(PATH_IN, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))


if __name__ == "__main__":
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)
