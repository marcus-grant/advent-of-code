# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import time
# import numpy as np
import pathlib
from typing import Union, List  # , Tuple, Dict, Literal, NewType, Optional

# Util imports
# from ..util.sols import cprint

# Solver ID Constants
DAY: str = "{{ day_str }}"
TITLE: str = "{{ day_title }}"
COMMENTS: str = """Put any extra comments for helper script here"""

# Types
PathLike = Union[str, pathlib.Path]


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # TODO: Implement solution here

    return 69


def part2(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # TODO: Implement solution here

    return 420


def run() -> None:
    PATH_EX = pathlib.Path(__file__).parent / "example.txt"
    PATH_IN = pathlib.Path(__file__).parent / "input.txt"
    print(f"\nDay {DAY} - {TITLE}\n")
    print("\nPart 1:\n")
    print(f"\nSolution on Example Data:\t{part1(PATH_EX, debug=True)}\n")
    print(f"\nSolution on Real Data:\t{part1(PATH_IN, debug=True)}\n")
    print("\nPart 2:\n")
    print(f"\nSolution on Example Data:\t{part2(PATH_EX, debug=True)}\n")
    print(f"\nSolution on Real Data:\t{part2(PATH_IN, debug=True)}\n")


if __name__ == "__main__":
    run()
