# Disabled imports
# import attrs
# import dataclasses
# import math
# import re
# import numpy as np
import functools
import math
import pathlib
from rich.console import Console
import time
from typing import Union, List, Optional, Dict  # , Tuple, Dict, Literal, NewType
import sys

console = Console()
cprint = console.print

# Util imports
# from ..util.sols import cprint

# Solver ID Constants
DAY: str = "07"
TITLE: str = "Bridge Repair"
COMMENTS: str = """
Interesting optimizations, otherwise standard dynamic programming (DP).
Try another optimization where you don't track sequences, just whether they're possible"""

# Types
PathLike = Union[str, pathlib.Path]


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def dp_recurse(target: int, nums: List[int], idx: int, current: int) -> List[str]:
    if idx == len(nums):  # Base case
        if current == target:
            return [""]  # Return empty - no need to append more operators
        return []  # Return None - no solution found

    # Initialization of recursive calls
    num_next = nums[idx]
    sequences = []

    # Possibility 1: Add (first since it takes less time)
    result_add = dp_recurse(target, nums, idx + 1, current + num_next)
    for seq in result_add:
        sequences.append("+" + seq)

    # Possibility 2: Multiply
    result_mul = dp_recurse(target, nums, idx + 1, current * num_next)
    for seq in result_mul:
        sequences.append("*" + seq)

    # If out of numbers, return the sequences
    return sequences


def cprint_seq(nums: List[int], seq: Optional[str]) -> None:
    cprint("Numbers Sequence:", style="blue", end="\t\t")
    cprint(" ".join(str(n) for n in nums))
    # Determine how many spaces to pad with first numbers
    pad = "\t\t" + (" " * (math.floor(math.log10(nums[0])) + 1))
    cprint("Operation Sequence:", style="blue", end=pad)
    if seq is None:
        cprint("No solution found", style="red")
        return
    s = ""
    for op in seq:
        if op == "+":
            s += " [green]+[/green] "
        elif op == "*":
            s += " [magenta]*[/magenta] "
        elif op == "|":
            s += " [yellow]|[/yellow] "
        else:
            msg = f"ERROR: Invalid operator: {op}\n{seq}"
            cprint(msg, style="red")
    s = s[1:-1]
    cprint(s)


def cprint_dp_result(res: int, i_res: int, nums: List[int], seqs: List[str]) -> None:
    cprint(f"\nResult #{i_res} = {res}", style="magenta")
    if len(seqs) == 0:
        cprint(f"No solution found for:\t\t{nums}", style="red")
    for j, seq in enumerate(seqs):
        cprint(f"Possible Sequence {j}:", style="blue")
        cprint_seq(nums, seq)


# NOTE: Unmemoized version of recursion took 83.336ms for Part 1
# NOTE: Memoized version of recursion took 176.220ms for Part 1 ?!?!
def part1(fpath: PathLike, debug: bool = False) -> int:
    # Parse input into a list[int] of results & list[list[int]] of operands per result
    lines = [line for line in read_lines(fpath)]
    numline = [[int(s.strip(":")) for s in line.split()] for line in lines]
    del lines
    results = [line[0] for line in numline]
    nums_list = [line[1:] for line in numline]
    del numline
    if debug:
        cprint("Results:", style="magenta")
        cprint(results, style="green")
        cprint("Operands:", style="magenta")
        cprint(nums_list, style="green")

    # Setup recurion for Dynamic Programming in loop for every result
    # FIXME: Perform all DP calculations in one go then print results
    valid_results = []
    sequence_count = 0
    for i, res in enumerate(results):
        ops_seq = dp_recurse(res, nums_list[i], 1, nums_list[i][0])
        sequence_count += len(ops_seq)
        if debug:
            cprint_dp_result(res, i, nums_list[i], ops_seq)
        if len(ops_seq) > 0:
            valid_results.append(res)

    if debug:
        cprint(f"Total Valid Sequences: {sequence_count}", style="blue")
        cprint("\nValid Results:", style="blue")
        cprint(", ".join(str(x) for x in valid_results), style="green")

    return sum(valid_results)


def dp_recurse3(target: int, nums: list[int], idx: int, current: int) -> list[str]:
    if idx == len(nums):  # base case
        if current == target:
            return [""]  # return empty - no need to append more operators
        return []  # return none - no solution found

    # initialization of recursive calls
    num_next = nums[idx]
    sequences = []

    # possibility 1: add (first since it takes less time)
    result_add = dp_recurse3(target, nums, idx + 1, current + num_next)
    for seq in result_add:
        sequences.append("+" + seq)

    # possibility 2: multiply
    result_mul = dp_recurse3(target, nums, idx + 1, current * num_next)
    for seq in result_mul:
        sequences.append("*" + seq)

    # possibility 3: concat
    result_cat = dp_recurse3(target, nums, idx + 1, int(str(current) + str(num_next)))
    for seq in result_cat:
        sequences.append("|" + seq)

    # if out of numbers, return the sequences
    return sequences


def dp_recurse_memo(target: int, nums: List[int], idx: int, current: int) -> List[str]:
    """
    Memoized recursive function to find all sequences of '+' and '*' operations
    that transform the list of numbers into the target value.
    """

    @functools.lru_cache(maxsize=None)
    def recurse(idx: int, current: int) -> tuple:
        # Base case: All numbers have been processed
        if idx == len(nums):
            if current == target:
                return ("",)  # Return a tuple with an empty string
            else:
                return ()  # Return an empty tuple indicating no valid sequence

        num_next = nums[idx]
        sequences = []

        # Possibility 1: Addition
        result_add = recurse(idx + 1, current + num_next)
        for seq in result_add:
            sequences.append("+" + seq)

        # Possibility 2: Multiplication
        result_mul = recurse(idx + 1, current * num_next)
        for seq in result_mul:
            sequences.append("*" + seq)

        # Possibility 3: Concatenation
        result_mul = recurse(idx + 1, int(str(current) + str(num_next)))
        for seq in result_mul:
            sequences.append("|" + seq)

        return tuple(sequences)  # Convert list to tuple for caching

    # Initiate recursion
    return list(recurse(idx, current))


def dp_tabulation(target: int, nums: List[int]) -> List[str]:
    if not nums:
        return []
    dp: List[Dict[int, List[str]]] = [{} for _ in range(len(nums) + 1)]
    dp[1][nums[0]] = [""]

    for i in range(1, len(nums)):
        current_num = nums[i]
        for acc_value, seq_list in dp[i].items():
            new_value = acc_value + current_num
            for seq in seq_list:
                dp[i + 1].setdefault(new_value, []).append(seq + "+" + str(current_num))

            new_value = acc_value * current_num
            for seq in seq_list:
                dp[i + 1].setdefault(new_value, []).append(seq + "*" + str(current_num))

            new_value = int(str(acc_value) + str(current_num))
            for seq in seq_list:
                dp[i + 1].setdefault(new_value, []).append(seq + "|" + str(current_num))

    return dp[-1].get(target, [])


# NOTE: Naive recursion took 6034.204 ms for Part 2
# NOTE: Memoized recursion took 10894.893 ms for Part 2 - I guess the overhead just is too much
# NOTE: Tabulation took... 13744.930 ms for Part 2 - This bares investigation
# NOTE: Try examining just checking if a sequence is possible don't track the sequence
def part2(fpath: PathLike, debug: bool = False) -> int:
    # Parse again
    lines = [line for line in read_lines(fpath)]
    numline = [[int(s.strip(":")) for s in line.split()] for line in lines]
    del lines
    results = [line[0] for line in numline]
    nums_list = [line[1:] for line in numline]
    del numline
    if debug:
        cprint("Results:", style="magenta")
        cprint(results, style="green")
        cprint("Operands:", style="magenta")
        cprint(nums_list, style="green")

    # Setup recurion for Dynamic Programming in loop for every result
    valid_results = []
    for i, res in enumerate(results):
        ops_seq = dp_recurse3(res, nums_list[i], 1, nums_list[i][0])
        if debug:
            cprint_dp_result(res, i, nums_list[i], ops_seq)
        if len(ops_seq) > 0:
            valid_results.append(res)

    if debug:
        cprint("\nValid Results:", style="blue")
        cprint(", ".join(str(x) for x in valid_results), style="green")

    # TODO: Implement solution here

    return sum(valid_results)


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

