import attrs
import dataclasses
import functools
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

def print_msg(msg: str, title: str="", style: str="yellow", justify: str="center"):
    title = None if len(title) == 0 else title
    panel = rich.panel.Panel.fit(msg, title=title, style=style)
    cprint(panel, justify=justify, new_line_start=True)

def read_input_lines(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

def process_records(lines: list[str], with_kern=False) -> list[Tuple[int, int]]:
    regex = r"\b\d+\b"
    time_strs = lines[0].split(":")[-1].strip()
    dist_strs = lines[1].split(":")[-1].strip()
    if not with_kern:
        times = list(map(int, re.findall(regex, time_strs)))
        dists = list(map(int, re.findall(regex, dist_strs)))
        return list(zip(times, dists))
    return (int(''.join(re.findall(regex, time_strs))),
            int(''.join(re.findall(regex, dist_strs))))
    

def print_records(records: list[Tuple[int, int]], **kwargs):
    from rich.table import Table
    # Check if the number of records matches the length of kwargs values
    if any(len(values) != len(records) for values in kwargs.values()):
        raise ValueError("Mismatch between len of records and kwarg values")

    table = Table(title="[bold yellow]Records[/bold yellow]")
    table.add_column("[bold red]Time[/bold red]", justify="center")
    table.add_column("[bold green]Distance[/bold green]", justify="center")

    # Add extra columns based on the kwargs keys
    for key in kwargs.keys():
        key_str = key[0].upper() + key[1:] # Capitalize first letter
        table.add_column(f"[blue]{key_str}[/blue]", justify="center")
    
    # Add rows based on the records and kwargs values
    for i, r in enumerate(records):
        row = [f"[red]{r[0]}[/red]", f"[green]{r[1]}[/green]"]
        for values in kwargs.values():
            row.append(f"[blue]{values[i]:.4g}[/blue]")
        table.add_row(*row)
    cprint(table, justify="center", new_line_start=True)

def calculate_winning_charge_time(
    time_max: int, dist_record: int
) -> Tuple[int, int]:
    # This is a quadratic equation to find minimum time
    # time_max, D: dist_record, time_min: t
    # The solution is t = T (+ or -) sqrt(T**2 - 4D)
    #                     --------------------------
    #                                  2
    # First, the discriminant is calculated & compared to 0
    discriminant = time_max**2 - 4*dist_record
    # If the discriminant is negative, then there is no (REAL) solution
    if discriminant < 0:
        raise ValueError("No real domain solution to beat the record")
    # If there is a real solution we can calculate it
    # To save time, we calculate the sqrt of the discriminant once
    # NOTE: the discriminant is the same as the square root term of the equation
    d2 = math.sqrt(discriminant)
    # Since return is ints, the min must be rounded up, opposite for max
    min_time_f, max_time_f = (time_max - d2) / 2, (time_max + d2) / 2
    # Now get the int versions
    min_time, max_time = math.ceil(min_time_f), math.floor(max_time_f)

    # Handle edge case where min or max times equal the record time.
    # This is because you need to beat the record, not tie it.
    min_time = min_time + 1 if math.isclose(min_time, min_time_f) else min_time
    max_time = max_time - 1 if math.isclose(max_time, max_time_f) else max_time
    
    return (math.ceil(min_time), max_time)

def integer_count_in_range(min: int, max: int) -> int:
    return max - min + 1

def part1(input_file: str) -> int:
    lines = read_input_lines(input_file)
    records = process_records(lines)
    print_msg("Race Records from Input")
    print_records(records)

    print_msg("Race Records with Calculated Winning Charge Times")
    winning_charge_time_range = [
        calculate_winning_charge_time(*r) for r in records]
    win_min_times = [t[0] for t in winning_charge_time_range]
    win_max_times = [t[1] for t in winning_charge_time_range]
    print_records(records, MinCharge=win_min_times, MaxCharge=win_max_times)
    
    print_msg("Race Records with Number of Possible Winning Charge Times")
    win_times_possibilities = [integer_count_in_range(*t)
                               for t in winning_charge_time_range]
    print_records(
        records,
        MinCharge=win_min_times,
        MaxCharge=win_max_times,
        NumCharges=win_times_possibilities)

    return functools.reduce(lambda x, y: x*y, win_times_possibilities)

def part2(input_file: str) -> int:
    # TODO: Come up with a better way to render this all
    lines = read_input_lines(input_file)
    race_record = process_records(lines, with_kern=True)
    print_msg(f"[bold magenta]{race_record[0]}ms[/bold magenta]",
              title="Race Time", style="bold blue")
    print_msg(f"[bold magenta]{race_record[1]}mm[/bold magenta]",
              title="Race Dist", style="bold blue")

    charge_range = calculate_winning_charge_time(*race_record)
    print_msg(f"[bold magenta]{charge_range[0]} ~ {charge_range[1]}ms[/bold magenta]",
              title="Charge Time to Beat Record", style="bold blue")
    
    charge_possibilities = integer_count_in_range(*charge_range)
    print_msg(f"[red]{charge_possibilities}[/red]",
                title="Charge Time Possibilities", style="bold blue")
    return charge_possibilities

def main():
    DAY = "06"
    EXAMPLE = f"{DAY}/example.txt"
    INPUT = f"{DAY}/input.txt"
    TITLES = [ # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE",
        "Part One - INPUT",
        "Part Two - EXAMPLE",
        "Part Two - INPUT",
    ]
    for t in TITLES:
        print_msg(t, style="bold green")
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
    cprint(
        rich.panel.Panel.fit(
            "[bold green]Advent of Code - Day 06 - Wait For It[/bold green]",
            style="bold red"),
        justify="center"
    )
    main()
    cprint(
        rich.panel.Panel.fit(
            "[bold red]Advent of Code - Day 06 - Complete![/bold red]",
            style="bold green"),
        justify="center"
    )