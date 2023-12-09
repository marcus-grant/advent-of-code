import attrs
import dataclasses
import math
from rich import print as rprint
from rich import console
import rich
import re
import time
from typing import Optional, List, Tuple, Dict, Union, NewType, Callable

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

def create_paths_dict(lines: list[str]) -> dict[str, tuple[str, str]]:
    paths = {}
    for l in lines[2:]:
        node, left, right = re.search('(...) = \((...), (...)\)', l).groups(0)
        paths[node] = (left, right)
    return paths

def traverse_paths(
        paths: dict[str, tuple[str, str]],
        sequence: str,
        start: str,
        end: str,
        callback: Optional[Callable[[str, str, str, str, str], None]] = None,
) -> list[str]:
    curr = start
    seq_idx = 0
    trace = []
    while curr != end:
        if seq_idx >= len(sequence): seq_idx = 0
        next_step = 1 if sequence[seq_idx] == 'R' else 0
        if callback is not None:
            callback(curr, next_step, paths[curr][0], paths[curr][1], trace)
        trace.append(curr)
        curr = paths[curr][next_step]
        seq_idx +=  1
    return trace

# TODO: Change to add step count
def trace_path(current, next_step, left, right):
    print('Current', current, 'NextStep?',
           next_step if next_step == 0 else 'right',
           ' | Left:', left, 'Right:', right,
           ' | Trace', trace)

def part1(f: str) -> int:
    lines = read_lines(f)
    sequence = lines[0]
    cprint(sequence)
    paths = create_paths_dict(lines)
    cprint(paths)
    trace = traverse_paths(paths, sequence, 'AAA', 'ZZZ')#, trace_path)
    cprint(trace)
    return len(trace)

def count_steps(paths, sequence, start, max_steps=100000):
    count = 0
    seq_idx = 0
    curr = start
    while not curr.endswith('Z') and count < max_steps:
        if seq_idx >= len(sequence): seq_idx = 0
        next_step = 1 if sequence[seq_idx] == 'R' else 0
        count += 1
        curr = paths[curr][next_step]
        seq_idx += 1
    return count

def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    return abs(a*b) // gcd(a, b)

def lcm_list(nums: list[int]) -> int:
    result = nums[0]
    for n in nums[1:]:
        result = lcm(result, n)
    return result

def part2(f: str) -> int:
    lines = read_lines(f)
    sequence = lines[0]
    cprint(sequence)
    paths = create_paths_dict(lines)
    cprint(paths)
    starts = [k for k in paths.keys() if k.endswith('A')]
    ends = [f"{k[:-1]}Z" for k in starts]
    cprint('Starts:', starts)
    cprint('Ends:', ends)
    step_counts = []
    for i in range(len(starts)):
        step_counts.append(count_steps(paths, sequence, starts[i]))
    cprint(step_counts)
    # Find LCM of step counts
    return lcm_list(step_counts)

def main():
    EXAMPLE = f"{DAY}/example.txt"
    EXAMPLE2 = f"{DAY}/example2.txt"
    EXAMPLE3 = f"{DAY}/example3.txt"
    INPUT = f"{DAY}/input.txt"
    TITLES = [ # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE1",
        "Part One - EXAMPLE2",
        "Part One - INPUT",
        "Part Two - EXAMPLE",
        "Part Two - INPUT",
    ]
    FILES = {
        TITLES[0]: (part1, EXAMPLE),
        TITLES[1]: (part1, EXAMPLE2),
        # TITLES[2]: (part1, INPUT),
        TITLES[3]: (part2, EXAMPLE3),
        TITLES[4]: (part2, INPUT),
    }
    for t, tup in FILES.items():
        print_panel(t, style="bold green")
        print_solution(f"{tup[0](tup[1])}", title=t)
        

if __name__ == "__main__":
    DAY = "08"
    DAY_TITLE = "Haunted Wasteland"
    msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE}[/bold green]" 
    print_panel(msg ,style="bold red")
    main()
    msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]" 
    print_panel(msg, style="bold green")