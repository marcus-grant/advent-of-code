import numpy as np
from typing import Tuple, Union
from pathlib import Path
from rich.console import Console

cnsl = Console()
cprint = cnsl.print

PathLike = Union[str, Path]


def read_fs(fpath: PathLike) -> np.ndarray:
    with open(fpath, "r") as f:
        fmap = f.read().strip()  # Single line

    fs = []
    for i in range(0, len(fmap), 2):  # Iterate over every 2 characters
        data_len = int(fmap[i])
        free_len = int(fmap[i + 1]) if i + 1 < len(fmap) else 0
        fs.extend([i // 2] * data_len)
        fs.extend([-1] * free_len)
    return np.array(fs, dtype=int)


def print_fs(fs: np.ndarray) -> None:
    for id in fs:
        if id == -1:
            cprint(".", end="", style="yellow")
        else:
            cprint(str(id) + "", end="")
    cprint("")


def next_free(fs: np.ndarray, i: int) -> int:
    mask = fs[i:] == -1
    if np.any(mask):
        return i + np.argmax(mask)
    return -1


def prior_data(fs: np.ndarray, i: int) -> int:
    mask = fs[: i + 1] != -1
    if np.any(mask):
        return np.where(mask)[0][-1]
    return -1


def defrag1(fs: np.ndarray, old_version: bool = False) -> None:
    next_fn = next_free
    prior_fn = prior_data
    i_free = next_fn(fs, 0)
    i_data = prior_fn(fs, len(fs) - 1)
    while i_free < i_data:
        fs[i_free] = fs[i_data]
        fs[i_data] = -1
        i_free = next_fn(fs, i_free)
        i_data = prior_fn(fs, i_data)


def calc_checksum(fs: np.ndarray) -> int:
    return np.sum(np.arange(len(fs)) * (fs != -1) * fs)


def part1(fpath: PathLike, debug: bool = False) -> int:
    fs = read_fs(fpath)
    defrag1(fs)
    if debug and "example" in str(fpath):
        print_fs(fs)
    return calc_checksum(fs)


def find_last_file(fs: np.ndarray, i_find: int) -> Tuple[int, int]:
    i_data = prior_data(fs, i_find)
    if i_data == -1:
        return -1, -1
    val_data = fs[i_data]
    size = 0
    while i_data - size >= 0 and fs[i_data - size] == val_data:
        size += 1
    return i_data - size + 1, size


def find_free_space(fs: np.ndarray, size: int) -> int:
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


def defrag2(fs: np.ndarray, debug: bool = False) -> None:
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
            fs[i_free : i_free + data_size] = fs[i_data : i_data + data_size]
            fs[i_data : i_data + data_size] = -1
        i_data -= 1


def part2(fpath: PathLike, debug: bool = False) -> int:
    fs = read_fs(fpath)
    defrag2(fs, debug)
    checksum = calc_checksum(fs)
    return checksum


def run() -> None:
    _EX = pathlib.Path(__file__).parent / "example.txt"
    _IN = pathlib.Path(__file__).parent / "input.txt"
    tstart = time.time()
    sol = part1(_EX)
    time_ms = 1000 * (time.time() - tstart)
    print(f"Part 1 example: {sol},\t\ttime: {time_ms:.3f} ms")
    tstart = time.time()
    sol = part1(_IN)
    time_ms = 1000 * (time.time() - tstart)
    print(f"Part 1 input: {sol},\t\ttime: {time_ms:.3f} ms")
    tstart = time.time()
    sol = part2(_EX)
    time_ms = 1000 * (time.time() - tstart)
    print(f"Part 2 example: {sol},\t\ttime: {time_ms:.3f} ms")
    tstart = time.time()
    sol = part2(_IN)
    time_ms = 1000 * (time.time() - tstart)
    print(f"Part 2 input: {sol},\t\ttime: {time_ms:.3f} ms")


if __name__ == "__main__":
    import pathlib
    import time

    run()
