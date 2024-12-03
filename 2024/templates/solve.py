# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import time
import numpy as np
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich import rule

from typing import Optional, List, Tuple, Dict, Union, Literal, NewType

console = Console()
cprint = console.print


def print_solution(
    sol: str,
    title: str = "",
    style: str = "bold red",
    justify: Literal["center", "left", "right"] = "center",
) -> None:
    # Construct the title message with conditional formatting
    if title:
        msg = f"[bold green]Solution to {title}[/bold green]"
    else:
        msg = "[bold green]Solution[/bold green]"

    # Create a Rich Panel with the solution text
    panel = Panel.fit(
        sol,
        title=msg,
        style=style,
        border_style=style,
        padding=(1, 2),  # Optional: Adds padding for better aesthetics
    )
    # Print the panel with specified justification
    cprint(panel, justify=justify, new_line_start=True)


def print_panel(
    msg: str,
    title: str = "",
    style: str = "yellow",
    justify: Literal["left", "center", "right"] = "center",
) -> None:
    """
    Print a styled panel using Rich.

    Args:
        msg (str): The message to display inside the panel.
        title (str, optional): The title of the panel. Defaults to "".
        style (str, optional): The style of the panel. Defaults to "yellow".
        justify (Literal["left", "center", "right"], optional):
            Text justification. Defaults to "center".
    """
    panel_title = title if title else None
    panel = Panel.fit(msg, title=panel_title, style=style)
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


def main(day_str: str) -> None:
    EXAMPLE = f"{day_str}/example.txt"
    INPUT = f"{day_str}/input.txt"
    TITLES = [  # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE",
        # NOTE: Uncomment these lines when ready to try real input or next part
        # "Part One - INPUT",
        # "Part Two - EXAMPLE",
        # "Part Two - INPUT",
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
    import argparse

    DAY = "{{ day_str }}"
    DAY_TITLE = "{{ day_title }}"
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
    main(DAY)
    # msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]"
    # print_panel(msg, style="bold green")
    cprint(rule.Rule(title=f"Advent of Code - Day {DAY} - Complete!"), style="red")
