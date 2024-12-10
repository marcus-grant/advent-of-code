from collections import deque as dq
from collections import defaultdict as dd
import pathlib
import time
from typing import Union, List, Tuple, Set
from rich.console import Console
import sys

console = Console()
cprint = console.print

# Solver ID Constants
DAY: str = "10"
TITLE: str = "Hoof It"
COMMENTS: str = """Not too bad once you figure out pathfinding is BFS traversal."""

# Types
PathLike = Union[str, pathlib.Path]
Height = int
Loc = Tuple[int, int]
Map = List[List[Height]]


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def find_trailheads(map: Map) -> List[Loc]:
    trailheads: List[Loc] = []
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == 0:
                trailheads.append((r, c))
    return trailheads


def find_neighbors(map: Map, loc: Loc) -> List[Loc]:
    """Find valid neighbors in cardinal directions."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    r, c = loc
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(map) and 0 <= nc < len(map[0]):
            neighbors.append((nr, nc))
    return neighbors


def gradient_ascent(map: Map, trailhead: Loc) -> Set[Loc]:
    """Given the list of heights, and start location, find all paths to peaks (9)"""
    # Determine neigbors (cardinal directions)
    q = dq([trailhead])
    visited = set([trailhead])
    peaks = set()

    while q:
        cur = q.popleft()
        cur_h = map[cur[0]][cur[1]]

        for n in find_neighbors(map, cur):
            nr, nc = n
            nh = map[nr][nc]
            if n not in visited and nh == cur_h + 1:
                visited.add(n)
                q.append(n)
                if nh == 9:
                    peaks.add(n)
    return peaks


def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # Parse the map
    map: Map = [[int(c) for c in line] for line in lines]
    if debug:
        cprint(map)

    # Find all trailheads (height 0)
    trailheads = find_trailheads(map)
    if debug:
        cprint(f"Trailheads: {trailheads}")

    # Calculate scores for each trailhead
    total_score = 0
    for trailhead in trailheads:
        peaks = gradient_ascent(map, trailhead)
        if debug:
            cprint(f"Trailhead {trailhead} can reach peaks: {peaks}")
        total_score += len(peaks)

    return total_score


def unique_paths(map: Map, trailhead: Loc) -> int:
    """Find all unique paths from a trailhead to peak (h = 9)"""
    paths = dd(set)  # Store paths keyed by end location (r,c)
    q = dq([(trailhead, [trailhead])])  # (Cur location, path so far)

    while q:
        cur, path = q.popleft()
        cur_h = map[cur[0]][cur[1]]

        for n in find_neighbors(map, cur):
            nr, nc = n
            nh = map[nr][nc]

            if n not in path and nh == cur_h + 1:
                new_path = path + [n]
                if nh == 9:
                    paths[n].add(tuple(new_path))
                else:
                    q.append((n, new_path))
    return sum(len(paths[peak]) for peak in paths)


def part2(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)

    # Parse the map
    map: Map = [[int(c) for c in line] for line in lines]
    if debug:
        cprint(map)

    # Find all trailheads (height 0)
    trailheads = find_trailheads(map)
    if debug:
        cprint(f"Trailheads: {trailheads}")

    # Calculate scores for each trailhead
    total_score = 0
    for trailhead in trailheads:
        score = unique_paths(map, trailhead)
        if debug:
            cprint(f"Trailhead {trailhead} has score: {score}")
        total_score += score

    return total_score


def bgrn(s) -> str:
    return f"\033[1;32m{s}\033[0m"


def mgta(s) -> str:
    return f"\033[35m{s}\033[0m"


def blue(s) -> str:
    return f"\033[34m{s}\033[0m"


def run(debug: bool = False) -> None:
    """Runs the solution for both Part 1 and Part 2, prints results with timing.
    Args:
        debug: If True, runs in debug mode with verbose output.
    """
    PATH_EX = pathlib.Path(__file__).parent / "example.txt"
    PATH_IN = pathlib.Path(__file__).parent / "input.txt"
    kw = {"debug": debug}

    print(f"\n{mgta('Day')} {bgrn(DAY)} - {mgta(TITLE)}\n")
    print(f"\n{bgrn('Part 1')}:\n")

    tstart = time.time()
    sol = part1(PATH_EX, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Example Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))

    tstart = time.time()
    sol = part1(PATH_IN, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))

    print(f"\n{bgrn('Part 2')}:\n")

    tstart = time.time()
    sol = part2(PATH_EX, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Example Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))

    tstart = time.time()
    sol = part2(PATH_IN, **kw)
    ms = f"{1000 * (time.time() - tstart):.3f}"
    print(f"\n{mgta('Solution with Real Data:')}\t{bgrn(sol)}\n")
    print(blue(f"Time taken (ms):\t\t{ms}\n"))


if __name__ == "__main__":
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)
