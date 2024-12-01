import argparse
import functools as ft
from rich import console, rule
import rich
from typing import Tuple

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

    
def read_lines_groups(fpath: str) -> Tuple[list[str], Tuple[int, ...]]:
    lines = []
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    groups = [l.split(' ')[1] for l in lines]
    groups = [tuple(int(n.strip()) for n in l.split(',')) for l in groups]
    lines = [l.split(' ')[0] for l in lines]
    return lines, groups

@ft.cache
def combos(line: str, groups: tuple[int, ...], i: int=0) -> int:
    if not groups: # If no groups size numbers left in list...
        # If there's also no broken springs left from ith char in the line...
        if not any(c == '#' for c in line[i:]):
            return 1 # Return 1, we've eliminated all remaining possibilities
        return 0
    
    # Grab first group size for this recursive call
    nxt = groups[0]
    while True:
        if i + nxt > len(line): # If the group size + current pos > len...
            return 0 # ...no possible places left.
        # Is i a possible location? Check searching # or ? till group size + i
        possible_loc = all(c in "#?" for c in line[i : i + nxt])
        # Can next (after group size) be an empty (. or ?) slot
        can_next_empty = i + nxt >= len(line) or line[i + nxt] != "#"
        # Now check if current is a possible spot for broken, and
        # the slot after this spot + group size can be empty
        if possible_loc and can_next_empty:
            # If so, recurse count by removing current group & mov line idx...
            count = combos(line, groups[1:], i + nxt + 1) # ... past grp size
            # If the current char is unknown slot...
            if line[i] == '?': # ...keep searching by recursing...
                count += combos(line, groups, i + 1) # count with the next char
            return count # We're done counting at this string index
        # If definitely a broken slot,
        if line[i] == '#': # We know, definitively not another combo can be here
            return 0
        # Nothing else to do, but increment the string index
        i += 1

def part1(fpath: str, verbose=True) -> int:
    lines, groups = read_lines_groups(fpath)
    verbose and cprint('Lines:', lines)
    verbose and cprint('Groups:', groups)

    all_combos = [combos(l, g) for l, g in zip(lines, groups)]
    if verbose:
        for l, g, c in zip(lines, groups, all_combos):
            cprint('Line:', l)
            cprint('Groups:', g)
            cprint('Combo Count:', c)

    return sum(all_combos)

def part2(fpath: str, verbose=True) -> int:
    lines, groups = read_lines_groups(fpath)
    verbose and cprint('Unfolded Lines:', lines)
    verbose and cprint('Unfolded Groups:', groups)
    verbose and print()

    lines = ['?'.join(5 * [sub]) for sub in lines]
    groups = tuple(g * 5 for g in groups)
    verbose and cprint('Lines:', lines)
    verbose and cprint('Groups:', groups)
    verbose and print()

    all_combos = [combos(l, g) for l, g in zip(lines, groups)]
    if verbose:
        for l, g, c in zip(lines, groups, all_combos):
            cprint('Line:', l)
            cprint('Groups:', g)
            cprint('Combo Count:', c)

    return sum(all_combos)

def main(arg):
    verbose = not arg.quiet
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
    DAY = "12"
    DAY_TITLE = "Hot Springs"
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