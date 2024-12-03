# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import time
import argparse
import numpy as np
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich import rule

from typing import Optional, List, Tuple, Dict, Union, Literal, NewType

console = Console()
cprint = console.print

# Solver ID Constants
DAY: str = "01"
TITLE: str = "Historian Hysteria"


def read_lines(fpath: str) -> list[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def part1(fpath: str, debug: bool = False) -> int:
    debug = False if debug is None else debug
    lines = read_lines(fpath)

    # Create the list1 & list2 for the 1st/2nd lists
    # if line.strip() is used to remove any empty lines
    # line.split takes either the left or right of the whitespace
    left = [int(line.split()[0]) for line in lines if line.strip()]
    right = [int(line.split()[1]) for line in lines if line.strip()]

    # Now as per the problem, sort each list ascending
    left = sorted(left)
    right = sorted(right)

    # Now we get the difference between the two
    diff = [abs(l - r) for l, r in zip(left, right)]

    # Part1's answer is the sum of differences
    answer = sum(diff)

    return answer


def part2(fpath: str, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # First parse the left and right lists of numbers
    left = [int(line.split()[0]) for line in lines if line.strip()]
    right = [int(line.split()[1]) for line in lines if line.strip()]

    # The left number for each row needs counting for occurrences on right list
    # Therefore it makes more sense to create a counting dictionary of the right
    right_counts = {}
    for x in right:
        if x not in right_counts:
            right_counts[x] = 1
        else:
            right_counts[x] += 1

    # For each left number, multiply its value by
    # that number's count in the right list
    answer = 0
    for x in left:
        if x in right_counts:
            answer += right_counts[x] * x

    return answer


def main(args):
    EXAMPLE = f"{DAY}/example.txt"
    INPUT = f"{DAY}/input.txt"
    TITLES = [  # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE",
        # NOTE: Uncomment these lines when ready to try real input or next part
        "Part One - INPUT",
        "Part Two - EXAMPLE",
        "Part Two - INPUT",
    ]
    for t in TITLES:
        print_panel(t, style="bold green")
        if "one" in t.lower() or "1" in t.lower():
            if "example" in t.lower():
                print_solution(f"{part1(EXAMPLE)}", title=t)
                continue
            print_solution(f"{part1(INPUT)}", title=t)
            continue
        if "example" in t.lower():
            print_solution(f"{part2(EXAMPLE)}", title=t)
            continue
        print_solution(f"{part2(INPUT)}", title=t)


if __name__ == "__main__":
    DAY = "01"
    DAY_TITLE = "Historian Hysteria"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Don't print debug lines of anything to the console",
    )
    args = parser.parse_args()
    # msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE}[/bold green]"
    cprint(rule.Rule(title=f"Advent of Code - Day {DAY} - {DAY_TITLE}"), style="red")
    # print_panel(msg ,style="bold red")
    main(args)
    # msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]"
    # print_panel(msg, style="bold green")
    cprint(rule.Rule(title=f"Advent of Code - Day {DAY} - Complete!"), style="red")
