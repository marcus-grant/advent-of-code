from attrs import asdict, define, make_class, Factory
from dataclasses import dataclass, field
from typing import List, Tuple
from colorama import Fore, Back, Style
from pprint import pprint
from pydantic import BaseModel

def print_solution(sol: str, title: str=""):
    s = f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.CYAN}Solution"
    if len(title) > 0:
        s += f" to {title}"
    s += f"{Style.RESET_ALL}: {Back.LIGHTCYAN_EX}{Fore.BLACK}{sol}{Style.RESET_ALL}"
    print(s)

def read_input(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

def part1(input_file: str) -> int:
    lines = read_input(input_file)
    return 0

def part2(input_file: str) -> int:
    lines = read_input(input_file)
    return 0

def main():
    EXAMPLE = "example.txt"
    INPUT = "input.txt"

    print()
    print("Part One - Example")
    print("==================")

    print()
    solution = part1(EXAMPLE)
    print_solution(f"\n{solution}\n", title="Part One (Example)")

    print()
    print("Part One - Input")
    print("=================")

    print()
    # TODO: Implement Part One Input

    print()
    print("Part Two - Example")
    print("==================")

    print()
    # TODO: Implement Part Two Example

    print()
    print("Part Two - Input")
    print("================")

    print()
    # TODO: Implement Part Two Input

if __name__ == "__main__":
    print('========================== Day 05 -  ===========================')
    main()
    print('====================== Day 05 - Complete =======================')

