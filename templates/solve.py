import attrs
import dataclasses
import math
from rich import print as rprint
from rich import console
import rich
import re
import time
from typing import Optional, List, Tuple, Dict, Union, NewType

console = console.Console()
cprint = console.print

def print_solution(sol: str, title: str=""):
    rprint(f"[b u red]Solution to {title}:[b u green]    {sol}    ")

def read_input_lines(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

def part1(input_file: str) -> int:
    lines = read_input_lines(input_file)

    return 0

def part2(input_file: str) -> int:
    lines = read_input_lines(input_file)

    return 0

def main():
    EXAMPLE = "{{ day_str }}/example.txt"
    INPUT = "{{ day_str }}/input.txt"

    print()
    print("Part One - Example")
    print("==================")

    print()
    solution = part1(EXAMPLE)
    print_solution(f"{solution}", title="Part One (Example)")

    # print()
    # print("Part One - Input")
    # print("================")

    # print()
    # solution = part1(INPUT)
    # print_solution(f"{solution}", title="Part One (INPUT)")

    # print()
    # print("Part Two - Example")
    # print("==================")

    # print()
    # solution = part2(EXAMPLE)
    # print_solution(f"{solution}", title="Part Two (Example)")

    # print()
    # print("Part Two - Input")
    # print("================")

    # print()
    # solution = part2(INPUT)
    # print_solution(f"{solution}", title="Part Two (Example)")
    print()


if __name__ == "__main__":
    print('==================== Day {{ day_str }} - {{ day_title }} =====================')
    main()
    print('====================== Day {{ day_str }} - Complete =======================')
