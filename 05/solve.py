from attrs import asdict, define, make_class, Factory
from colorama import Fore, Back, Style
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, NewType, Union
import re
from rich import print as rprint
from rich.console import Console
from rich.pretty import pprint
import rich
import time

console = Console()

def print_solution(sol: str, title: str=""):
    rprint(f"[bold][underline][red]Solution to {title}:[/red][green]    {sol}[/green]    [/underline][/bold]")

def read_input(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = [l.strip() for l in f.read().splitlines()]
        # Check if the last or first line is empty
        lines = lines[1:] if lines[0] == "" else lines
        lines = lines[:-1] if lines[-1] == "" else lines
    return lines

MAP_IDX_DST_START = 0
MAP_IDX_SRC_START = 1
MAP_IDX_RANGE_LEN = 2

def parse_maps(lines: list[str]) -> list[list[Tuple[int, int, int]]]:
    i = 2 # Maps start at line 3 (index 2)
    # Now go through every line and for every line with numbers,
    # parse the numbers into a map (list[int]) and add it to the list of maps
    maps = []
    while i < len(lines):
        maps.append([])
        i += 1
        while i < len(lines) and not lines[i] == "":
            dst, src, rln = map(int, lines[i].split())
            maps[-1].append((dst, src, rln))
            i += 1
        i += 1 # Skip the map name line
    return maps

def print_maps_table(maps: list[list[Tuple[int, int, int]]]):
    from rich.table import Table
    table = Table(title="Maps")
    table.add_column("DestStart", justify="center")
    table.add_column("SrcStart", justify="center")
    table.add_column("RangeLen", justify="center")
    for rules in maps:
        for r in rules:
            table.add_row(
                f"[blue]{r[MAP_IDX_DST_START]}[/blue]",
                f"[red]{r[MAP_IDX_SRC_START]}[/red]",
                f"[green]{r[MAP_IDX_RANGE_LEN]}[/green]"
            )
    rprint(table)

def map_seed_to_location(
        seed: int, maps: list[list[Tuple[int, int, int]]]
) -> int:
    current = seed
    for rules in maps:
        for r in rules:
            dst = r[MAP_IDX_DST_START]
            src = r[MAP_IDX_SRC_START]
            rln = r[MAP_IDX_RANGE_LEN]
            if src <= current < src + rln:
                current = (dst - src) + current
                break
    return current

def part1(input_file: str) -> int:
    lines = read_input(input_file)

    rprint('[cyan]Here are all the seeds:[/cyan]')
    print()
    seeds = [int(s) for s in lines[0].split(" ")[1:] if s != ""]
    console.print(seeds, style="bold green")

    print()
    console.print('[cyan]Here is the table of all maps:[/cyan]' )
    print()
    maps = parse_maps(lines)
    print_maps_table(maps)

    print()
    rprint('[cyan]Here are all the mapped seed -> locations:[/cyan]')
    print()
    seed_locations = [(s, map_seed_to_location(s, maps)) for s in seeds]
    for s, loc in seed_locations:
        console.print(f"[bold][red]{s}[/red] -> [green]{loc}[/green][/bold]")
    print()

    return min([loc for _, loc in seed_locations])



def part2(input_file: str) -> int:
    lines = read_input(input_file)
    return 0

def main():
    EXAMPLE = "05/example.txt"
    INPUT = "05/input.txt"

    print()
    print("Part One - Example")
    print("==================")

    print()
    solution = part1(EXAMPLE)
    print_solution(f"{solution}", title="Part One (Example)")

    print()
    print("Part One - Input")
    print("=================")

    print()
    solution = part1(INPUT)
    print_solution(f"{solution}", title="Part One (INPUT)")

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

def alt():
    with open("05/example.txt") as fin:
        lines = fin.read().strip().split("\n")

    seeds = list(map(int, lines[0].split(" ")[1:]))

    # Generate all the mappings
    maps = []

    i = 2
    while i < len(lines):
        maps.append([])

        i += 1
        while i < len(lines) and not lines[i] == "":
            dstStart, srcStart, rangeLen = map(int, lines[i].split())
            maps[-1].append((dstStart, srcStart, rangeLen))
            i += 1

        i += 1


    def findLoc(seed):
        curNum = seed

        for m in maps:
            for dstStart, srcStart, rangeLen in m:
                if srcStart <= curNum < srcStart + rangeLen:
                    curNum = dstStart + (curNum - srcStart)
                    break

        return curNum


    locs = []
    for seed in seeds:
        loc = findLoc(seed)
        locs.append(loc)

    print(min(locs))

if __name__ == "__main__":
    print('========================== Day 05 -  ===========================')
    main()
    # alt()
    print('====================== Day 05 - Complete =======================')

