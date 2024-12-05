# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import time
# import numpy as np
import pathlib
from rich.console import Console
import sys
from typing import Union, List  # , Tuple, Dict, Literal, NewType, Optional

# Util imports
# from ..util.sols import cprint

console = Console()
cprint = console.print

# Solver ID Constants
DAY: str = "05"
TITLE: str = "Print Queue"
COMMENTS: str = """Put any extra comments for helper script here"""

# Types
PathLike = Union[str, pathlib.Path]


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # First find the line that devides the two sections
    divider = -1
    for line_idx, line in enumerate(lines):
        if len(line) == 0:
            divider = line_idx
    assert divider >= 0, "No divider line found"

    # Split lines into updates sections as a list of list of ints
    updates = [[int(x) for x in s.split(",")] for s in lines[divider + 1 :]]
    if debug:
        cprint("\nRules:\n", ", ".join(lines[:divider]))
        # cprint("\nUpdates:\n", updates)
        cprint("\nUpdates:\n", style="bold blue")
        for i, up in enumerate(updates):
            cprint(f"Update #{i}: {up}")

    # Create a rules dictionary, first num as key, second as value
    # This way when we look at a number in the updates section...
    # we look up the earlier number as a key to find the numbers that
    # should appear afterwards
    rules = set()
    for rule in lines[:divider]:
        k, v = map(int, rule.split("|"))
        rules.add((k, v))

    if debug:
        cprint("\nRules Set:\n", rules)

    # Check each update
    mid_pgs = []
    for iu, update in enumerate(updates):
        # Map page#s to their positions in the current update line
        pg_posns = {pg: i for i, pg in enumerate(update)}
        is_valid = True

        # Check each rule
        for pg1, pg2 in rules:
            if pg1 in pg_posns and pg2 in pg_posns:
                # Both pages of rule in the current update line so check order
                if pg_posns[pg1] > pg_posns[pg2]:
                    if debug:  # Print debug message about broken rule
                        msg = f"Rule {pg1}|{pg2} broken in update: {update}"
                        cprint(msg, style="bold red")
                    is_valid = False  # Rule broken in this update
                    break  # No need to check more rules

        # If current update is valid
        if is_valid:
            # Find the middle page number
            count_pgs = len(update)
            mid_idx = count_pgs // 2  # For odd count, this is the middle page
            mid_pg = update[mid_idx]
            mid_pgs.append(mid_pg)
            if debug:
                cprint(f"Update {iu} valid, Mid Page: {mid_pg}", style="green")

    # All the middle pages of valid updates have been found
    # Sum them for the answer to part1
    return sum(mid_pgs)


def part2(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # TODO: Implement solution here

    return 420


def bgrn(s) -> str:
    return f"\033[1;32m{s}\033[0m"


def mgta(s) -> str:
    return f"\033[35m{s}\033[0m"


def run(debug: bool = False) -> None:
    PATH_EX = pathlib.Path(__file__).parent / "example.txt"
    PATH_IN = pathlib.Path(__file__).parent / "input.txt"
    kw = {"debug": debug}

    print(f"\n{mgta('Day')} {bgrn(DAY)} - {mgta(TITLE)}\n")
    print(f"\n{bgrn('Part 1')}:\n")
    sol = part1(PATH_EX, **kw)
    print(f"\n{mgta('Solution with Example Data:')}\t{bgrn(sol)}\n")
    sol = part1(PATH_IN, **kw)
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(f"\n{bgrn('Part 2:')}\n")
    sol = part2(PATH_EX, **kw)
    print(f"\n{mgta('Solution on Example Data')}:\t{bgrn(sol)}\n")
    # print(f"\nSolution on Real Data:\t{part2(PATH_IN, debug=True)}\n")


if __name__ == "__main__":
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)

