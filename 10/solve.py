import attrs
from collections import deque
import dataclasses
import math
import numpy as np
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

def read_input_lines(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

PIPE_ENCODING = {'.':0, '|':1, '-':2, 'L':3, 'J':4, '7':5, 'F':6, 'S':7}
PIPE_DECODING = ['.', '|', '-', 'L', 'J', '7', 'F', 'S']
PIPE_DECODING_SHAPE = [' ', '│', '─', '└', '┘', '┐', '┌', 'S']
PIPE_NBRS = {
    PIPE_ENCODING['.']: [],
    PIPE_ENCODING['|']: [(1, 0), (-1, 0)],
    PIPE_ENCODING['-']: [(0, 1), (0, -1)],
    PIPE_ENCODING['L']: [(-1, 0), (0, 1)],
    PIPE_ENCODING['J']: [(-1, 0), (0, -1)],
    PIPE_ENCODING['7']: [(1, 0), (0, -1)],
    PIPE_ENCODING['F']: [(1, 0), (0, 1)],
}

def encode_lines(lines: List[str]) -> np.matrix:
    return np.array( [ [PIPE_ENCODING[c] for c in l] for l in lines] )

def decode_matrix(
        mat: np.matrix, decoder: list[str]=PIPE_DECODING
) -> list[list[str]]: return [''.join( [decoder[c] for c in r] ) for r in mat]

def print_matrix(mat: np.matrix) -> None:
    decoded = decode_matrix(mat, PIPE_DECODING_SHAPE)
    for r in decoded:
        print(r)

def get_neighbors(
        mat: np.matrix, pos: Tuple[int, int]
) -> List[Tuple[int, int]]:
    res = []
    if mat[pos] == PIPE_ENCODING['S']:
        return get_neighbors_diff_start(mat, pos)
    for dr, dc in list(get_neighbors_diff(mat, pos)):
        rr, cc = pos[0] + dr, pos[1] + dc
        if not (0 <= rr < mat.shape[0] and 0 <= cc < mat.shape[1]):
            continue
        res.append((rr, cc))
    return res

def get_neighbors_diff_start(
        mat: np.matrix, pos: Tuple[int, int]
) -> List[Tuple[int, int]]:
    if mat[pos[0]][pos[1]] != PIPE_ENCODING['S']:
        raise ValueError("Position is not a start position")
    res = []
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        rr, cc = pos[0] + dr, pos[1] + dc
        if not (0 <= rr < mat.shape[0] and 0 <= cc < mat.shape[1]):
            continue
        if pos in list(get_neighbors(mat, (rr, cc))):
            res.append((rr, cc))
    return res

def get_neighbors_diff(
        mat: np.matrix, pos: Tuple[int, int]
)-> List[Tuple[int, int]]:
    return PIPE_NBRS[ mat[pos] ]

def distances_from_start(mat: np.matrix, start: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    seen = set()
    distances = {}
    q = deque([(start, 0)])
    while len(q) > 0:
        pos, dist = q.popleft()
        if pos in seen:
            continue
        seen.add(pos)
        distances[pos] = dist
        for nbr in get_neighbors(mat, pos):
            q.append((nbr, dist + 1))
    return distances

def part1(input_file: str) -> int:
    lines = read_input_lines(input_file)
    matrix = encode_lines(lines)
    cprint('Graphic Pipe Map:')
    print_matrix(matrix)

    start = np.argwhere(matrix == PIPE_ENCODING['S'])
    if len(start) != 1:
        raise ValueError("There should be EXACTLY ONE start position")
    start = (start[0][0], start[0][1])
    cprint('Start:', start)

    distances = distances_from_start(matrix, start)
    # cprint('Distances from start:')
    # cprint(distances)
    return max([d for d in distances.values()])

# TODO: Needs fixing, see out of tree solution to adapt later then visualize
def part2(input_file: str) -> int:
    lines = read_input_lines(input_file)
    matrix = encode_lines(lines)
    cprint('Graphic Pipe Map:')
    print_matrix(matrix)

    return 0

def main():
    EXAMPLE = f"{DAY}/example.txt"
    EXAMPLE2 = f"{DAY}/example2.txt"
    INPUT = f"{DAY}/input.txt"
    TITLES = [ # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE 1",
        "Part One - INPUT",
        "Part Two - EXAMPLE 2",
        "Part Two - INPUT",
    ]
    FILES = {
        TITLES[0]: (part1, EXAMPLE),
        TITLES[2]: (part1, INPUT),
        TITLES[3]: (part2, EXAMPLE2),
        # TITLES[4]: (part2, INPUT),
    }
    for t, tup in FILES.items():
        print_panel(t, style="bold green")
        print_solution(f"{tup[0](tup[1])}", title=t)
        

if __name__ == "__main__":
    DAY = "10"
    DAY_TITLE = "Pipe Maze"
    msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE}[/bold green]" 
    print_panel(msg ,style="bold red")
    main()
    msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]" 
    print_panel(msg, style="bold green")