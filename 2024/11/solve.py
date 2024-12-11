# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import numpy as np
from collections import deque as dq
import pathlib
import time
from typing import Union, List, Deque, Tuple  # Dict, Literal, NewType, Optional
from rich.console import Console
import sys

cprint = Console().print


# Solver ID Constants
DAY: str = "11"
TITLE: str = "Plutonian Pebbles"
COMMENTS: str = """Put any extra comments for helper script here"""

# Types
PathLike = Union[str, pathlib.Path]


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def parse_stones(fpath: PathLike) -> Deque[int]:
    stones_str = read_lines(fpath)[0]
    stones = dq([int(s) for s in stones_str.split()])
    return stones


def apply_rule2(stone_int: int) -> List[int]:
    stone_str = str(stone_int)
    mid = len(stone_str) // 2
    left = int(stone_str[:mid]) if stone_str[:mid] else 0
    right = int(stone_str[mid:]) if stone_str[mid:] else 0
    return [left, right]


def blink(stones: Deque[int]) -> Deque[int]:
    new_stones = dq()
    while stones:
        stone = stones.popleft()
        if stone == 0:  # Rule #1
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:  # Rule #2
            new_stones.extend(apply_rule2(stone))
        else:  # Rule #3
            new_stones.append(stone * 2024)
    return new_stones


# NOTE: 334341 is too high your range was one too high for blink_count
def part1(fpath: PathLike, debug: bool = False) -> int:
    stones = parse_stones(fpath)
    blink_count = 7 if "example" in str(fpath) else 25
    for _ in range(blink_count):
        if debug:
            cprint(stones)
        stones = blink(stones)

    return len(stones)


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
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)

