from collections import defaultdict
import pathlib
import time
from typing import Union, List, Dict
from rich.console import Console
import sys

cprint = Console().print


# Solver ID Constants
DAY: str = "11"
TITLE: str = "Plutonian Pebbles"
COMMENTS: str = """Sped up by many magnitudes on larger loops by using a map instead of Deque List."""

# Types
PathLike = Union[str, pathlib.Path]


def parse_stones(fpath: PathLike) -> Dict[int, int]:
    stones_map = defaultdict(int)
    for stone in open(fpath).read().split():
        stones_map[int(stone)] += 1
    return stones_map


def process_stone(stone: int) -> List[int]:
    str_stone = str(stone)
    len_stone = len(str_stone)
    if stone == 0:
        return [1]
    elif len_stone % 2 == 0:
        half = len(str_stone) // 2
        stone1, stone2 = int(str_stone[:half]), int(str_stone[half:])
        return [stone1, stone2]
    else:
        return [stone * 2024]


def blink(stones_map: Dict[int, int]) -> Dict[int, int]:
    new_stones_map = defaultdict(int)
    for stone, count in stones_map.items():
        new_stones = process_stone(stone)
        for new_stone in new_stones:
            new_stones_map[new_stone] += count
    return new_stones_map


# NOTE: 334341 is too high your range was one too high for blink_count
def part1(fpath: PathLike, debug: bool = False) -> int:
    stones_map = parse_stones(fpath)
    for _ in range(25):
        stones_map = blink(stones_map)
    return sum(list(stones_map.values()))


def part2(fpath: PathLike, debug: bool = False) -> int:
    stones_map = parse_stones(fpath)
    for _ in range(75):
        stones_map = blink(stones_map)
    if debug:
        cprint("\nAfter 75 blinks, there are this many unique stones:", end=" ")
        cprint(len(stones_map), style="bold green")
    return sum(list(stones_map.values()))


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

    tstart = time.time()
    sol = part2(PATH_IN, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))


if __name__ == "__main__":
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)

