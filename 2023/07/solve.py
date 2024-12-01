import attrs
import dataclasses
import functools
import math
import random
from rich import print as rprint
from rich import console
import rich
import re
import time
from typing import Any, Optional, List, Tuple, Dict, Union
from typing import Literal, LiteralString, NewType

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

def memoize(fn):
    cache = {}
    def wrapper(string):
        if string not in cache:
            cache[string] = fn(string)
        return cache[string]
    return wrapper

@memoize
def count_cards(hand: str) -> list[int]:
    # Craete a count list for numbers of each character
    counts = {} # First count using a dict
    for c in hand: # Each key is a card character in the hand string
        counts[c] = counts.get(c, 0) + 1 # Each value is its count
    return sorted(counts.values(), reverse=True) # Counts as sorted list ASC.

def score_hand(hand: str) -> int:
    counts = count_cards(hand)
    if counts[0] == 5: return                    7 # Five of a kind (highest)
    if counts[0] == 4: return                    6 # Four of a kind
    if counts[0] == 3 and counts[1] == 2: return 5 # Full house
    if counts[0] == 3: return                    4 # Three of a kind
    if counts[0] == 2 and counts[1] == 2: return 3 # Two pair
    if counts[0] == 2: return                    2 # One pair
    return                                       1 # High card

def name_score(score: int) -> str:
    return ['High Card', '1 Pair', '2 Pair', 'Triplet',
            'Full House', '4 of a Kind', '5 of a Kind'][score - 1]

def compare_hands(a: str, b: str) -> int:
    # First determine if the hand scores are different as it's the first rule
    if score_hand(a) > score_hand(b): return 1
    if score_hand(a) < score_hand(b): return -1
    # If you're here we need to compare the high card (1st card, then 2nd, etc)
    # We do this by scoring 
    rank = lambda c: '23456789TJQKA'.index(c)
    for a, b in zip(map(rank, a), map(rank, b)):
        if a > b: return 1
        if a < b: return -1
    # Finally return 0 because hands are equal
    return 0

def part1(f: str) -> int:
    games = [(g[0], int(g[1])) for g in (l.split(' ') for l in read_lines(f))]
    # cprint(games)
    # cprint([(g[0], name_score(score_hand(g[0]))) for g in games])
    games_sorted = sorted(
        games, #reverse=True,
        key=functools.cmp_to_key(lambda a, b: compare_hands(a[0], b[0])))
    # cprint(games_sorted)
    return sum(g[1] * (i + 1) for i, g in enumerate(games_sorted))

# @memoize
def count_cards_wild(hand: str) -> Tuple[list[int], int]:
    wilds = 0
    counts = {} # First count using a dict
    for c in hand:
        if c == 'J': wilds += 1
        else: counts[c] = counts.get(c, 0) + 1
    if len(counts) == 0: return [0], wilds
    return sorted(counts.values(), reverse=True), wilds

# @memoize
def score_hand_wild(hand: str) -> int:
    # Similar to before but now we need to track wilds
    counts, wilds = count_cards_wild(hand)

    # First few cases are treated largely the same,
    # we just include wilds in the counts as they can be used to increase counts
    if counts[0] + wilds >= 5 or wilds >= 5: return 7
    if counts[0] + wilds >= 4 or wilds >= 4: return 6

    # Full House & Triplets requires special handling
    if counts[0] + wilds >= 3:
        rm_wilds = counts[0] + wilds - 3
        if len(counts) >= 2 and counts[1] + rm_wilds >= 2 or rm_wilds >= 2:
            return 5
        return 4
    
    # Continue as before
    if counts[0] + wilds >= 2 or wilds >= 2: return 3
    if counts[0] + wilds >= 1 or wilds >= 1: return 2
    return 1

def compare_hands_wild(a: str, b: str) -> int:
    # First determine if the hand scores are different as it's the first rule
    if score_hand_wild(a) > score_hand_wild(b): return 1
    if score_hand_wild(a) < score_hand_wild(b): return -1
    # If you're here we need to compare the high card (1st card, then 2nd, etc)
    # We do this by scoring 
    rank = lambda c: 'J23456789TQKA'.index(c)
    for a, b in zip(map(rank, a), map(rank, b)):
        if a > b: return 1
        if a < b: return -1
    # Finally return 0 because hands are equal
    return 0

def part2(f: str) -> int:
    games = [(g[0], int(g[1])) for g in (l.split(' ') for l in read_lines(f))]
    # cprint([(g[0], name_score(score_hand_wild(g[0]))) for g in games])
    games_sorted = sorted(
        games, #reverse=True,
        key=functools.cmp_to_key(lambda a, b: compare_hands_wild(a[0], b[0])))
    # cprint(games_sorted)
    return sum(g[1] * (i + 1) for i, g in enumerate(games_sorted))

def main():
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
                print_solution(f"{part1(EXAMPLE)}", title=t)
                continue
            print_solution(f"{part1(INPUT)}", title=t)
            continue
        if 'example' in t.lower():
            print_solution(f"{part2(EXAMPLE)}", title=t)
            continue
        print_solution(f"{part2(INPUT)}", title=t)
        

if __name__ == "__main__":
    DAY = "07"
    DAY_TITLE = "Camel Cards"
    msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE} [/bold green]" 
    print_panel(msg ,style="bold red")
    main()
    msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]" 
    print_panel(msg, style="bold green")
