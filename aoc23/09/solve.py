# Just setup for a nicer solving experience
import argparse
from rich import print as rprint
from rich import console
import rich
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

def read_lines(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

# Real work starts here
def successive_diffs(series: list[int]) -> list[list[int]]:
    diffed = series # Start with differential order of 0 ie no diff
    res = [diffed]
    while not all([d == 0 for d in diffed]):
        diffed = [diffed[i+1] - diffed[i] for i in range(len(diffed)-1)]
        res.append(diffed)
    return res

def poly_interpolate(diffs: list[list[int]]) -> list[list[int]]:
    diffs[-1].append(0)
    prev_diff = diffs[-1]
    for diff in diffs[-2::-1]:
        diff.append(prev_diff[-1] + diff[-1])
        prev_diff = diff
    return diffs

def print_diff_pyramid(diffs: list[list[int]]) -> None:
    for diff in diffs:
        cprint(diff, justify="center", end="\n", soft_wrap=True)

def part1(f: str, verbose=True) -> int:
    all_series = [[int(s) for s in l.split(' ')] for l in read_lines(f)]
    all_diffs = [successive_diffs(s) for s in all_series]
    all_diffs_interp = [poly_interpolate(d) for d in all_diffs]

    # Note if disabling verbose printing these lines are the ones to skip
    if verbose:
        for diff in all_diffs_interp:
            print_panel(f"Differentials after Interpolation of Next Value")
            print_diff_pyramid(diff)
            print_panel(f"[bold green]{diff[0][-1]}[/bold green]",
                        title="Interpolated Next Value", style="yellow")

    return sum(diff[0][-1] for diff in all_diffs_interp)

def poly_interpolate_reverse(diffs: list[list[int]]) -> list[list[int]]:
    diffs[-1].insert(0, 0)
    prev_diff = diffs[-1]
    for diff in diffs[-2::-1]:
        diff.insert(0, diff[0] - prev_diff[0])
        prev_diff = diff
    return diffs

def part2(f: str, verbose) -> int:
    all_series = [[int(s) for s in l.split(' ')] for l in read_lines(f)]
    all_diffs = [successive_diffs(s) for s in all_series]
    all_diffs_interp = [poly_interpolate_reverse(d) for d in all_diffs]

    if verbose:
        for diff in all_diffs:
            print_panel(f"Differentials after Interpolation of Preceeding Value")
            print_diff_pyramid(diff)
            print_panel(f"[bold green]{diff[0][0]}[/bold green]",
                        title="Interpolated Preceeding Value", style="yellow")

    return sum([d[0][0] for d in all_diffs_interp])

# Real work ends here, this just sets up solution order
def main(verbose: bool=True):
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
                print_solution(f"{part1(EXAMPLE, verbose)}", title=t)
                continue
            print_solution(f"{part1(INPUT, verbose)}", title=t)
            continue
        if 'example' in t.lower():
            print_solution(f"{part2(EXAMPLE, verbose)}", title=t)
            continue
        print_solution(f"{part2(INPUT, verbose)}", title=t)
        

if __name__ == "__main__":
    DAY = "09"
    DAY_TITLE = "Mirage Maintenance"
    # Parse single set of arguments -v --verbose as optional bool
    parser = argparse.ArgumentParser(description=f"Advent of Code 2023 Day {DAY}")
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Don't print verbose output"
    )
    args = parser.parse_args()
    msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE}[/bold green]" 
    print_panel(msg ,style="bold red")
    main(not args.quiet)
    msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]" 
    print_panel(msg, style="bold green")