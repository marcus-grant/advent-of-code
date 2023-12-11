import attrs
import dataclasses
import numpy as np
import math
from rich import print as rprint
from rich import console
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

def part1(fpath: str) -> int:
    lines = read_lines(fpath)

    return 0

def part2(fpath: str) -> int:
    lines = read_lines(fpath)

    return 0

def main():
    EXAMPLE = f"{DAY}/example.txt"
    INPUT = f"{DAY}/input.txt"
    TITLES = [ # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE",
        # "Part One - INPUT",
        # "Part Two - EXAMPLE",
        # "Part Two - INPUT",
    ]
    for t in TITLES:
        print_panel(t, style="bold green")
        if 'one' in t.lower() or '1' in t.lower():
            if 'example' in t.lower():
                print_solution(f"{part1(EXAMPLE)}", title=t)
                continue
            print_solution(f"{part1(INPUT)}", title=t)
            continue
        if 'example' in t.lower():
            print_solution(f"{part2(EXAMPLE)}", title=t)
            continue
        print_solution(f"{part2(INPUT)}", title=t)
        

if __name__ == "__main__":
    DAY = "{{ day_str }}"
    DAY_TITLE = "{{ day_title }}"
    msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE}[/bold green]" 
    print_panel(msg ,style="bold red")
    main()
    msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]" 
    print_panel(msg, style="bold green")
