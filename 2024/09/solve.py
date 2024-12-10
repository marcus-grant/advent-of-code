# import numpy as np
import pathlib
from rich.console import Console
import time
from typing import Union, List, Tuple
import sys

cnsl = Console()
cprint = cnsl.print

# Solver ID Constants
DAY: str = "09"
TITLE: str = "Disk Fragmenter"
COMMENTS: str = """
Check out the profiler, range(len - 1, -1, -1) is slow!
Lots of optimizations possible.
Good place to try numpy or numba for speedups.
And different data structures.
"""

# Types
PathLike = Union[str, pathlib.Path]


def read_fs(fpath: PathLike) -> List[int]:
    with open(fpath, "r") as f:
        fmap = f.read().strip()  # Single line

    fs: List[int] = []
    for i in range(0, len(fmap), 2):  # Iterate over every 2 characters
        data_len = int(fmap[i])
        free_len = int(fmap[i + 1]) if i + 1 < len(fmap) else 0
        fs += [i // 2] * data_len
        fs += [-1] * free_len
    return fs


def print_fs(fs: List[int]) -> None:
    for id in fs:
        if id == -1:
            cprint(".", end="", style="yellow")
        else:
            cprint(str(id) + "", end="")
    cprint("")


def next_free_old(fs: List[int], i: int) -> int:
    # NOTE: Holy shit reverse range() is slow if called thousands+ times
    for i in range(i, len(fs)):
        if fs[i] == -1:
            return i
    raise ValueError(f"No free space found after {i}")


def prior_data_old(fs: List[int], i: int) -> int:
    # NOTE: Is it len being called so much?
    fslen = len(fs)
    for i in range(fslen - 1, -1, -1):
        if fs[i] != -1:
            return i
    raise ValueError(f"No data found before {i}")


def next_free(fs: List[int], i: int) -> int:
    fslen = len(fs)
    while i < fslen:
        if fs[i] == -1:
            return i
        i += 1
    return -1


def prior_data(fs: List[int], i: int) -> int:
    while i >= 0:
        if fs[i] != -1:
            return i
        i -= 1
    return -1


def defrag1(fs: List[int], old_version: bool = False) -> None:
    next_fn = next_free if not old_version else next_free_old
    prior_fn = prior_data if not old_version else prior_data_old
    i_free = next_fn(fs, 0)  # type: ignore
    i_data = prior_fn(fs, len(fs) - 1)  # type: ignore
    while i_free < i_data:
        fs[i_free] = fs[i_data]
        fs[i_data] = -1
        i_free = next_fn(fs, i_free)  # type: ignore
        i_data = prior_fn(fs, i_data)  # type: ignore


def calc_checksum(fs: List[int]) -> int:
    return sum(i * id for i, id in enumerate(fs) if id != -1)


def part1(fpath: PathLike, debug: bool = False) -> int:
    fs = read_fs(fpath)

    # Defrag
    defrag1(fs)
    if debug and "example" in str(fpath):
        print_fs(fs)  # Disable for input.txt, too large

    # Calculate checksum
    return calc_checksum(fs)


def find_last_file(fs: List[int], i_find: int) -> Tuple[int, int]:
    """Starting from i search backwards for nearest continous file blocks.
    Return a tuple with start index and length of file block."""
    i_data = prior_data(fs, i_find)
    val_data = fs[i_data]
    size = 0
    while i_data - size >= 0 and fs[i_data - size] == val_data:
        size += 1
    if i_data - size < 0:
        return -1, -1
    return i_data - size + 1, size


def find_free_space(fs: List[int], size: int) -> int:
    lenfs = len(fs)
    i_free = next_free(fs, 0)
    i_data = i_free + 1
    while i_free + size >= i_data and i_free >= 0:
        while i_data < lenfs and fs[i_data] == -1:
            i_data += 1
        if i_data - i_free >= size:
            return i_free
        i_free = next_free(fs, i_data)
        i_data = i_free + 1
    return -1


def defrag2(fs: List[int], debug: bool = False) -> None:
    i_data = len(fs) - 1
    i_free = 0
    prev_idata = i_data
    while i_data >= 0:
        if debug and prev_idata - i_data > 2000:
            prev_idata = i_data
            cprint(f"Current i_data: {i_data}", style="yellow")
        if debug and len(fs) < 100:
            print_fs(fs)
        i_data, data_size = find_last_file(fs, i_data)
        i_free = find_free_space(fs, data_size)
        if i_free >= 0 and i_free < i_data:  # free space found
            for i in range(data_size):
                fs[i_free + i] = fs[i_data + i]  # Copy data into free space
                fs[i_data + i] = -1  # Delete original
        # Move i_data to previous block
        i_data -= 1


def part2(fpath: PathLike, debug: bool = False) -> int:
    fs = read_fs(fpath)
    defrag2(fs, debug)
    checksum = calc_checksum(fs)
    return checksum


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


def profile_index_funcs_in_defrag1(fpath: PathLike) -> None:
    import cProfile
    import pstats
    from io import StringIO

    pr = cProfile.Profile()
    pr.enable()
    # fs = read_fs(fpath)
    # cprint("\nProfiling defrag1 with old functions", style="yellow")
    # defrag1(fs, old_version=True)
    # fs = read_fs(fpath)
    # cprint("\nProfiling defrag1 with new functions", style="yellow")
    # defrag1(fs, old_version=False)
    fs = read_fs(fpath)
    cprint("\nProfiling defrag2", style="yellow")
    defrag2(fs)
    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats()
    print(s.getvalue())


if __name__ == "__main__":
    # Check for single --debug or -d flag without argparse
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    # run(debug)
    if debug:
        msg = "\nRunning profiler"
        cprint(msg, style="magenta")
        profile_index_funcs_in_defrag1(pathlib.Path(__file__).parent / "input.txt")
