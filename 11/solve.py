import argparse
import attrs
import dataclasses
import math
import numpy as np
from rich import print as rprint
from rich import console
from rich import rule
import rich
import re
import time
from typing import Optional, List, Tuple, Dict, Union, NewType

console = console.Console()
cprint = console.print


def print_solution(
        sol: str, title: str="", style: str="bold red", justify: str="center"
) -> None:
    msg = '[bold green]Solution'
    msg += f' to {title}[/bold green]' if len(title) > 0 else '[/bold green]'
    panel = rich.panel.Panel.fit(sol, title=msg, style="bold red")
    cprint(panel, justify=justify, new_line_start=True)

def print_panel(msg: str, title: str="",
                style: str="yellow", justify: str="center") -> None:
    title = None if len(title) == 0 else title
    panel = rich.panel.Panel.fit(msg, title=title, style=style)
    cprint(panel, justify=justify, new_line_start=True)

def read_lines(fpath: str) -> list[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines

Coord = NewType("Coord", tuple[int, int]) # (row, col)
Galaxy = NewType("Galaxy", Coord)
Galaxies = NewType("Galaxies", list[Galaxy])

# def expand_vertical(galaxies: Galaxies, at_row: int) -> Galaxies:
#     return [(g[0] + 1 if g[0] > at_row else g[0], g[1]) for g in galaxies]

# def expand_horizontal(galaxies: Galaxies, at_col: int) -> Galaxies:
#     return [(g[0], g[1] + 1) for g in galaxies if g[1] > at_col]

def empty_axes(galaxies: Galaxies) -> Tuple[list[int], list[int]]:
    occupied_rows = set([g[0] for g in galaxies])
    occupied_cols = set([g[1] for g in galaxies])
    empty_rows, empty_cols = [], []
    for i in range(max(occupied_rows)):
        if i not in occupied_rows: empty_rows.append(i)
    for i in range(max(occupied_cols)):
        if i not in occupied_cols: empty_cols.append(i)
    return (empty_rows, empty_cols)

def expand_universe(galaxies: Galaxies, amount: int = 2) -> Galaxies:
    empty_rows, empty_cols = empty_axes(galaxies)
    amount -= 1
    for r in reversed(empty_rows):
        galaxies = [(g[0] + amount if g[0] > r else g[0], g[1])
                    for g in galaxies]
    for c in reversed(empty_cols):
        galaxies = [(g[0], g[1] + amount if g[1] > c else g[1])
                    for g in galaxies]
    return galaxies

def distance(g1: Galaxy, g2: Galaxy) -> int:
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])

def part1(fpath: str, quiet: bool=False) -> int:
    verbose = not quiet
    galaxies = []
    for r, line in enumerate(read_lines(fpath)):
        for c, char in enumerate(line):
            if char == '#':
                galaxies.append((r, c))
    if verbose: cprint(galaxies)

    if verbose: cprint(empty_axes(galaxies))
    expanded = expand_universe(galaxies)
    if verbose: cprint(expanded)

    pairs_dict = {}
    for i in range(len(expanded)):
        for j in range(i + 1, len(expanded)):
            g1, g2 = expanded[i], expanded[j]
            pairs_dict[(g1, g2)] = distance(g1, g2)
    if verbose: cprint(pairs_dict)

    return sum(pairs_dict.values())

def part2(fpath: str, quiet: bool=False) -> int:
    verbose = not quiet
    galaxies = []
    for r, line in enumerate(read_lines(fpath)):
        for c, char in enumerate(line):
            if char == '#':
                galaxies.append((r, c))
    if verbose: cprint(galaxies)

    if verbose: cprint(empty_axes(galaxies))
    expansion_amount = 10 if 'example' in fpath else 10**6
    expanded = expand_universe(galaxies, expansion_amount)
    if verbose: cprint(expanded)

    pairs_dict = {}
    for i in range(len(expanded)):
        for j in range(i + 1, len(expanded)):
            g1, g2 = expanded[i], expanded[j]
            pairs_dict[(g1, g2)] = distance(g1, g2)
    if verbose: cprint(pairs_dict)

    return sum(pairs_dict.values())

def main(args):
    q = args.quiet
    EXAMPLE = f"{DAY}/example.txt"
    INPUT = f"{DAY}/input.txt"
    TITLES = [ # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE",
        "Part One - INPUT",
        "Part Two - EXAMPLE",
        "Part Two - INPUT",
    ]
    for t in TITLES:
        print_panel(t, style="bold green")
        if 'one' in t.lower() or '1' in t.lower():
            if 'example' in t.lower():
                print_solution(f"{part1(EXAMPLE, q)}", title=t)
                continue
            print_solution(f"{part1(INPUT, q)}", title=t)
            continue
        if 'example' in t.lower():
            print_solution(f"{part2(EXAMPLE, q)}", title=t)
            continue
        print_solution(f"{part2(INPUT, q)}", title=t)
        

if __name__ == "__main__":
    DAY = "11"
    DAY_TITLE = "Cosmic Expansion"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Don't print debug lines of anything to the console")
    args = parser.parse_args()
    # msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE}[/bold green]" 
    cprint(rule.Rule(title=f"Advent of Code - Day {DAY} - {DAY_TITLE}"), style="red")
    # print_panel(msg ,style="bold red")
    main(args)
    # msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]" 
    # print_panel(msg, style="bold green")
    cprint(rule.Rule(title=f"Advent of Code - Day {DAY} - Complete!"), style="red")
