import numpy as np
import pathlib
from scipy.ndimage import label
from scipy.signal import convolve2d
import time
from typing import Union, List, Dict, Any
from numpy.typing import NDArray
import sys

# Solver ID Constants
DAY: str = "12"
TITLE: str = "Garden Groups"
COMMENTS: str = """
I realized that with scipy a REALLLY fast generalized solution comes from
convolving the grid to calculate the edges of every grouped plot.
This is a REALLY GOOD solution to write about.
As such read the README.
NOTE:
Ran out of time on a dfs based solution with Location.neighbors while
working on the Grid and Location utility classes.
Continue the work on the next grid based problem"""

# Types
PathLike = Union[str, pathlib.Path]
ArrayMask = NDArray[np.bool_]


def read_lines(fpath: PathLike) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def debug_print_conv(**kw: Dict[str, Any]) -> None:
    msg = f"Region {kw['i']} (Value {kw['v']}):\t"
    msg += f"Area={kw['a']}, Perim.={kw['p']}, Cost={kw['c']}"
    print(msg)


def process_region(region: np.ndarray, unique_val: str, debug: bool = False):
    """
    Processes connected regions of a specific value in the grid.
    Computes region properties like area, perimeter, and convolution results.
    Returns a list of dictionaries with the metrics for each region.
    """
    results = []  # Collect results for each region
    # Label connected regions
    labeled_array, num_features = label(region == unique_val)  # type: ignore
    # Iterate over each region of the labeled array
    for i in range(1, num_features + 1):
        # Isolate region of interest into a binary mask
        binary_mask = labeled_array == i
        # Convolve region with kernels
        h_kern, v_kern, c_kern = [[1, -1]], [[1], [-1]], [[-1, 1], [1, -1]]
        h_conv = convolve2d(binary_mask, h_kern)
        v_conv = convolve2d(binary_mask, v_kern)
        c_conv = convolve2d(binary_mask, c_kern)
        # Calculate region properties
        perimeter = np.count_nonzero(h_conv) + np.count_nonzero(v_conv)
        sides_count = np.abs(c_conv).sum()
        area = binary_mask.sum()
        cost = area * perimeter
        # Add metrics to results
        results.append(
            {
                "region_index": i,
                "value": unique_val,
                "area": area,
                "perimeter": perimeter,
                "cost": cost,
                "sides": sides_count,
                "h_conv": h_conv,
                "v_conv": v_conv,
                "c_conv": c_conv,
            }
        )
        if debug:
            debug_print_conv(i=i, v=unique_val, a=area, p=perimeter, c=cost)  # type: ignore
        if results is None:
            raise ValueError("Results is None")
    return results


def part1(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)  # Parse input to ndarray grid
    grid = np.array([list(line.strip()) for line in lines])
    total_cost = 0  # Init total cost tracker
    for unique_val in np.unique(grid):  # Iterate over unique values
        results = process_region(grid, unique_val, debug)
        total_cost += sum(r["cost"] for r in results)  # type: ignore
    return total_cost


def part2(fpath: PathLike, debug: bool = False) -> int:
    lines = read_lines(fpath)  # Parse input to ndarray grid
    grid = np.array([list(line.strip()) for line in lines])
    total_cost = 0
    for unique_val in np.unique(grid):
        results = process_region(grid, unique_val, debug)
        total_cost += sum(r["sides"] * r["area"] for r in results)
    return total_cost


def run(debug: bool = False) -> None:
    """Runs the solution for both Part 1 and Part 2, prints results with timing.
    Args:
        debug: If True, runs in debug mode with verbose output.
    """
    PATH_EX = pathlib.Path(__file__).parent / "example.txt"
    PATH_IN = pathlib.Path(__file__).parent / "input.txt"
    bgrn = lambda s: f"\033[1;32m{s}\033[0m"  # noqa
    mgta = lambda s: f"\033[35m{s}\033[0m"  # noqa
    blue = lambda s: f"\033[34m{s}\033[0m"  # noqa

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
