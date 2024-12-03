# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import time
# import numpy as np
# from typing import Optional, List, Tuple, Dict, Union, Literal, NewType

# Util imports
from ..util.sols import cprint


# Solver ID Constants
DAY: str = "{{ day_str }}"
TITLE: str = "{{ day_title }}"


def read_lines(fpath: str) -> list[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def part1(fpath: str) -> int:
    lines = read_lines(fpath)

    # TODO: Implement solution here

    return 0


def part2(fpath: str) -> int:
    lines = read_lines(fpath)

    # TODO: Implement solution here

    return 0


def run() -> None:
    cprint(f"Day {DAY} - {TITLE}", style="bold red")
    cprint()
    cprint("Part 1:")
    cprint()
    cprint("Solution with Example Data:")
    cprint(f"{part1('input.txt')}", style="bold green")
    cprint()
    cprint("Solution with Real Data:")
    cprint(f"{part1('input.txt')}", style="bold green")
    cprint()
    cprint("Part 2:")
    cprint()
    cprint("Solution with Example Data:")
    cprint(f"{part2('example.txt')}", style="bold green")
    cprint()
    cprint("Solution with Real Data:")
    cprint(f"{part2('input.txt')}", style="bold green")
    cprint()


if __name__ == "__main__":
    run()
