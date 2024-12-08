import pathlib
import time
from typing import Union, List, Tuple, Set, Dict  # , Literal, NewType, Optional
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
COMMENTS: str = """Got rushed, please revisit and solve from beginninig. Used brute force to save time"""

# Types
PathLike = Union[str, pathlib.Path]
Location = Tuple[int, int]
AntennaPairAntinodes = Tuple[Location, Location]


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def parse_map(map_data: List[str]) -> List[Tuple[int, int, str]]:
    """
    Parse input map to extract antenna locations and frequencies

    Returns list of (x, y, frequency) tuples
    """
    antennas = []
    for y, line in enumerate(map_data):
        for x, char in enumerate(line):
            if char.isalnum():
                antennas.append((x, y, char))
    return antennas


def calculate_antinodes(
    antennas: List[Tuple[int, int, str]], map_size: int
) -> Set[Tuple[int, int]]:
    """
    Calculate unique antinode locations

    Antinodes are created by extending the vector between antennas
    of the EXACT SAME frequency, but only within grid bounds
    """
    antinodes = set()

    for i, (x1, y1, f1) in enumerate(antennas):
        for x2, y2, f2 in antennas[i + 1 :]:
            # Only process antennas with EXACT SAME frequency
            if f1 != f2:
                continue

            # Calculate vector between antennas
            dx = x2 - x1
            dy = y2 - y1

            # Extend vector in both directions, but only if within grid bounds
            # One direction
            nx1, ny1 = x1 - dx, y1 - dy
            if 0 <= nx1 < map_size and 0 <= ny1 < map_size:
                antinodes.add((nx1, ny1))

            # Other direction
            nx2, ny2 = x2 + dx, y2 + dy
            if 0 <= nx2 < map_size and 0 <= ny2 < map_size:
                antinodes.add((nx2, ny2))

    return antinodes


def part1(fpath, debug: bool = False) -> int:
    """
    Solve Part 1: Count unique antinode locations
    """
    lines = read_lines(fpath)
    antennas = parse_map(lines)

    if debug:
        print(f"Found {len(antennas)} antennas")
        print("Antennas:", antennas)

    antinodes = calculate_antinodes(antennas, len(lines))

    if debug:
        print("Antinodes:", antinodes)
        print(f"Total unique antinodes: {len(antinodes)}")

    return len(antinodes)


def is_collinear(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> bool:
    """
    Check if three points are collinear with improved precision
    """
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c

    # Check exact vertical line case
    if x1 == x2 == x3:
        return True

    # Check exact horizontal line case
    if y1 == y2 == y3:
        return True

    # Check diagonal case using cross product method
    # This handles imprecise floating-point comparisons and diagonal lines
    cross_product = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    return abs(cross_product) < 1e-10  # Allow for tiny floating-point imprecision


def calculate_antinodes2(
    antennas: List[Tuple[int, int, str]], map_size: int, debug: bool = False
) -> Set[Tuple[int, int]]:
    """
    Calculate unique antinode locations with updated model.
    """
    antinodes = set()

    # Group antennas by frequency
    freq_groups = {}
    for x, y, f in antennas:
        if f not in freq_groups:
            freq_groups[f] = []
        freq_groups[f].append((x, y))

    # Process each frequency group
    for freq, group in freq_groups.items():
        if debug:
            print(f"Processing frequency {freq} with {len(group)} antennas")

        # Add all antennas as antinodes (if more than one exists for this frequency)
        if len(group) > 1:
            for x, y in group:
                antinodes.add((x, y))

        # Check all pairs of antennas to find aligned antinodes
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                x1, y1 = group[i]
                x2, y2 = group[j]

                # Calculate the vector between the two antennas
                dx, dy = x2 - x1, y2 - y1

                # Extend the line in both directions
                k = 1
                while True:
                    nx1, ny1 = x1 - k * dx, y1 - k * dy
                    nx2, ny2 = x2 + k * dx, y2 + k * dy

                    if 0 <= nx1 < map_size and 0 <= ny1 < map_size:
                        antinodes.add((nx1, ny1))
                    if 0 <= nx2 < map_size and 0 <= ny2 < map_size:
                        antinodes.add((nx2, ny2))

                    # Stop extending if out of bounds
                    if not (0 <= nx1 < map_size and 0 <= ny1 < map_size) and not (
                        0 <= nx2 < map_size and 0 <= ny2 < map_size
                    ):
                        break

                    k += 1

    return antinodes


def part2(fpath, debug: bool = False) -> int:
    """
    Solve Part 2: Count unique antinode locations with updated model
    """
    lines = read_lines(fpath)
    antennas = parse_map(lines)

    if debug:
        print(f"Found {len(antennas)} antennas")
        print("Antennas:", antennas)

    antinodes = calculate_antinodes2(antennas, len(lines), debug)

    if debug:
        print("Antinodes:", antinodes)
        print(f"Total unique antinodes: {len(antinodes)}")

    return len(antinodes)


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
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)

