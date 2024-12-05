# import numpy as np
from collections import defaultdict
from collections import deque as dq
import pathlib
from rich.console import Console
import sys
import time
from typing import Union, List, Set, Tuple  # , Dict, Literal, NewType, Optional

# Util imports
# from ..util.sols import cprint

console = Console()
cprint = console.print

# Solver ID Constants
DAY: str = "05"
TITLE: str = "Print Queue"
COMMENTS: str = """Didn't go too badly, would like to try speeding up with numpy"""

# Types
PathLike = Union[str, pathlib.Path]
Rule = Tuple[int, int]
RuleSet = Set[Rule]
Update = List[int]
UpdateList = List[Update]


def read_lines(fpath: PathLike) -> List[str]:
    """Reads lines from a file and returns them as a list of strings.
    Args:
        fpath: Path to the input file.
    Returns:
        A list of strings representing the lines in the file.
    """
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def find_divider(lines: List[str]) -> int:
    """Finds the index of the first empty line in the list of lines, which serves as a divider between sections.
    Args:
        lines: A list of strings representing the input lines.
    Returns:
        The index of the first empty line.
    Raises:
        ValueError: If no empty line is found in the input.
    """
    for line_idx, line in enumerate(lines):
        if len(line) == 0:
            return line_idx
    raise ValueError("No divider line found")


def read_rules(lines: List[str], debug: bool = False) -> RuleSet:
    """Parses the ordering rules from the input lines up to the divider index.
    Args:
        lines: List of input lines.
        debug: If True, prints debugging information.
    Returns:
        A set of rules, where each rule is a tuple (X, Y) where X precede Y.
    """
    rules = set()
    for rule in lines[: find_divider(lines)]:
        k, v = map(int, rule.split("|"))
        rules.add((k, v))

    if debug:
        cprint("\nRules Set:\n", rules)
    return rules


def read_updates(lines: List[str], debug: bool = False) -> UpdateList:
    """Parses the updates from the input lines starting after the divider index.
    Args:
        lines: List of input lines.
        debug: If True, prints debugging information.
    Returns:
        A list of updates, where each update is a list of page numbers.
    """
    divider = find_divider(lines)
    updates = [[int(x) for x in s.split(",")] for s in lines[divider + 1 :]]
    if debug:
        cprint("\nRules:\n", ", ".join(lines[:divider]))
        # cprint("\nUpdates:\n", updates)
        cprint("\nUpdates:\n", style="bold blue")
        for i, up in enumerate(updates):
            cprint(f"Update #{i}: {up}")
    return updates


def update_valid(update: Update, rules: RuleSet, debug=False) -> bool:
    """Checks if a given update is valid according to the ordering rules.
    Args:
        update: A list of page numbers representing the update.
        rules: A set of ordering rules.
        debug: If True, prints debugging information.
    Returns:
        True if the update is valid, False otherwise.
    """
    # Map page#s to their positions in the current update line
    pg_posns = {pg: i for i, pg in enumerate(update)}
    is_valid = True
    # Check each rule
    for pg1, pg2 in rules:
        if pg1 in pg_posns and pg2 in pg_posns:
            # Both pages of rule in the current update line so check order
            if pg_posns[pg1] > pg_posns[pg2]:
                if debug:  # Print debug message about broken rule
                    msg = f"Rule {pg1}|{pg2} broken in update: {update}"
                    cprint(msg, style="bold red")
                is_valid = False  # Rule broken in this update
                break  # No need to check more rules
    return is_valid


def correct_update(update: Update, rules: RuleSet, debug=False) -> Update:
    """Corrects invalid update by reordering pages according to ordering rules.
    Performs a topological sort of pages in update to satisfy ordering constraints.
    Args:
        update: A list of page numbers representing the invalid update.
        rules: A set of ordering rules.
        debug: If True, prints debugging information.
    Returns:
        A list of page numbers representing the corrected update.
    Raises:
        ValueError: If a cycle is detected in the ordering rules.
    """
    # Build graph (an adjacency list) and in_degrees for each
    graph = defaultdict(set)  # Node -> set of nodes it points to
    in_deg = defaultdict(int)  # Node -> # incoming edges

    pages = set(update)

    # Init in_deg for all pages in the update with zeros
    for pg in update:
        in_deg[pg] = 0

    # Generate the graph & in_deg counts
    for pg1, pg2 in rules:
        # Both pages must be in the update to use the rule
        if pg1 in pages and pg2 in pages:
            # If the rule applies, add an edge from pg1 to pg2
            graph[pg1].add(pg2)
            # Track the incoming edges to pg2
            in_deg[pg2] += 1

    # Queue for pages with no incoming edges, setting up the DFS traversal
    # Also I hate typing queue & deque, so use aliases q & dq
    # Sounds the same when spoken
    q = dq([pg for pg in update if in_deg[pg] == 0])
    corrected_update = []

    while q:
        node = q.popleft()  # Like in a DFS, pop the node from the queue
        corrected_update.append(node)  # Once dq'd, it's in the correct order
        for neighbor in graph[node]:
            # Reduce degree of the neighbor
            in_deg[neighbor] -= 1
            # If the neighbor has no more incoming edges
            if in_deg[neighbor] == 0:
                q.append(neighbor)  # add it to the queue

    # Please Odin, let there be no cycles
    if len(corrected_update) != len(update):
        raise ValueError("Cycle detected in update: {}".format(update))

    if debug:
        cprint(f"Corrected Update: {corrected_update}", style="magenta")

    return corrected_update


def part1(fpath: PathLike, debug: bool = False) -> int:
    """Solves Part 1 Day 05 of Advent of Code 2024.
    Reads the input file, parses the rules and updates,
    and calculates the sum of
    the middle pages of valid updates according to the rules.
    Args:
        fpath: Path to the input file.
        debug: If True, prints debugging information.
    Returns:
        The sum of the middle pages of valid updates.
    """
    lines = read_lines(fpath)
    rules = read_rules(lines, debug)
    updates = read_updates(lines, debug)

    # Check each update and initialize the list of middle pages
    mid_pgs = []
    for iu, update in enumerate(updates):
        # If current update is valid
        if update_valid(update, rules, debug):
            # Find the middle page number
            mid_idx = len(update) // 2  # For odd count, this is the middle page
            mid_pg = update[mid_idx]
            mid_pgs.append(mid_pg)
            if debug:  # Print debug message about valid update
                cprint(f"Update {iu} valid, Mid Page: {mid_pg}", style="green")

    # All the middle pages of valid updates have been found
    # Sum them for the answer to part1
    return sum(mid_pgs)


def part2(fpath: PathLike, debug: bool = False) -> int:
    """Solves Part 2 of the problem.
    Reads the input file, parses the rules & updates, corrects invalid updates,
    & calculates the sum of the middle pages of corrected updates.
    Args:
        fpath: Path to the input file.
        debug: If True, prints debugging information.
    Returns:
        The sum of the middle pages of corrected updates.
    """
    # First read the file and extract the rules and updates data structures
    lines = read_lines(fpath)
    rules = read_rules(lines, debug)
    updates = read_updates(lines, debug)

    # This time we track mid pages of corrected INVALID updates
    mid_pgs = []
    for iu, update in enumerate(updates):
        # TODO: Find a cleaner way to arrange to make more DRY
        # If current update is valid
        if not update_valid(update, rules, debug):
            # Correct the update by using page order rules
            corrected = correct_update(update, rules, debug)
            mid_idx = len(update) // 2
            mid_pg = corrected[mid_idx]
            mid_pgs.append(mid_pg)
            if debug:
                msg = f"Update {iu} corrected to {corrected}, Mid Page: {mid_pg}"
                cprint(msg, style="magenta")

        else:  # Update is valid only matters for debugging
            if debug:  # Print debug message about valid update
                mid_pg = update[len(update) // 2]
                cprint(f"Update {iu} valid, Mid Page: {mid_pg}", style="green")

    return sum(mid_pgs)


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

