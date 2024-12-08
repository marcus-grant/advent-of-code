# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import numpy as np
import pathlib
import time
from typing import Union, List, Tuple, Dict  # , Literal, NewType, Optional
import sys

from rich import print as rprint
from rich.console import Console

console = Console()
cprint = console.print

# Util imports
# from ..util.sols import cprint

# Solver ID Constants
DAY: str = "08"
TITLE: str = "Resonant Collinearity"
COMMENTS: str = """Put any extra comments for helper script here"""

# Types
PathLike = Union[str, pathlib.Path]
Location = Tuple[int, int]
AntennaPairAntinodes = Tuple[Location, Location]


class Antenna:
    def __init__(self, freq: str, row: int, column: int):
        self.freq = freq
        self.loc: Location = (row, column)

        # def locate_antinodes(self, other: "Antenna") -> AntennaPairAntinodes:
        #     anode1 = (self.loc[0] - other.loc[0], self.loc[1] - other.loc[1])
        #     anode2 = (other.loc[0] - self.loc[0], other.loc[1] - self.loc[1])
        #     return anode1, anode2

    def locate_antinodes(self, other: "Antenna") -> List[Location]:
        # Calculate potential antinodes
        antinodes = []
        if self.freq == other.freq:
            # Calculate midpoint
            mid_row = (self.loc[0] + other.loc[0]) // 2
            mid_col = (self.loc[1] + other.loc[1]) // 2
            # Check if midpoint is valid
            if (self.loc[0] - other.loc[0]) % 2 == 0 and (
                self.loc[1] - other.loc[1]
            ) % 2 == 0:
                antinodes.append((mid_row, mid_col))
        return antinodes

    def __repr__(self):
        return f"Antenna(freq={self.freq}, loc={self.loc})"


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def parse_map(map_data):
    antennas = []
    for y, line in enumerate(map_data):
        for x, char in enumerate(line):
            if char.isalnum():
                antennas.append((x, y, char))
    return antennas


def calculate_antinodes(antennas, map_size):
    antinodes = set()
    for x, y, freq in antennas:
        # Determine the range based on the frequency character
        if freq.islower():
            range_radius = ord(freq) - ord("a") + 1
        elif freq.isupper():
            range_radius = ord(freq) - ord("A") + 1
        else:
            continue  # Skip non-alphabetic characters

        # Calculate affected positions
        for dx in range(-range_radius, range_radius + 1):
            for dy in range(-range_radius, range_radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < map_size and 0 <= ny < map_size:
                    antinodes.add((nx, ny))
    return antinodes


def count_unique_antinodes(map_data):
    antennas = parse_map(map_data)
    antinodes = calculate_antinodes(antennas, len(map_data))
    return len(antinodes)


# NOTE: 410 Too high
def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)
    count = count_unique_antinodes(lines)
    return count
    # antennas = [
    #     Antenna(freq, i_row, i_col)
    #     for i_row, line in enumerate(lines)
    #     for i_col, freq in enumerate(line)
    #     if freq.isalnum()
    # ]

    # antenna_pairs: List[Tuple[Antenna, Antenna]] = []
    # for i, a1 in enumerate(antennas):
    #     for a2 in antennas[i + 1 :]:
    #         if a1.freq == a2.freq:
    #             antenna_pairs.append((a1, a2))
    # matching_count = len(antenna_pairs)

    # if debug:
    #     cprint("Some stats from data:", style="magenta")
    #     cprint("Number of antennas:\t\t", len(antennas))
    #     cprint("Unique frequencies:\t\t", len(set(a.freq for a in antennas)))
    #     # Calculate all the pairs of same frequency antennas
    #     cprint("Matching pairs of antennas:\t", matching_count)
    #     cprint("Most possible antinodes:\t", matching_count * 2)
    #     msg = "NOTE: Some antinodes can overlap or exist outside grid."
    #     cprint(msg, justify="center", style="yellow")

    # antinode_locs = set()
    # for i, a1 in enumerate(antennas):
    #     for a2 in antennas[i + 1 :]:
    #         antinodes = a1.locate_antinodes(a2)
    #         for node in antinodes:
    #             if 0 <= node[0] < len(lines) and 0 <= node[1] < len(lines[0]):
    #                 antinode_locs.add(node)

    # cprint("\nAntinode Locations:", antinode_locs, style="magenta")

    # # DELETEME: ?
    # # Get unique antinode locations & filter out ones on antennas or outside map
    # # uniques = set(antinode_locs)
    # # r_max, c_max = len(lines), len(lines[0])
    # # inbounds = [(r, c) for r, c in uniques if 0 <= r < r_max and 0 <= c < c_max]

    # if debug:
    #     cprint("\nSome stats from antinodes:", style="magenta")
    #     cprint("Number of antinodes:\t\t", len(antinode_locs))

    # return len(antinode_locs)


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

