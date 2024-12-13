# Disabled imports
import re
import numpy as np
import sys
import pathlib
import time
from typing import Union, List, Tuple

# Solver ID Constants
DAY: str = "13"
TITLE: str = "Claw Contraption"
COMMENTS: str = """
Check the comments section at bottom for failed attempts at
making linear algebra using numpy work.
The problem ultimately has to do with floating point errors.
I suspect there's a way to still use numpy but
it just doesn't seem worth it.
It's worth remembering this lesson in the future when using numpy.
"""

# Types
PathLike = Union[str, pathlib.Path]


def solve(aX, aY, bX, bY, pX, pY, conversion_error=0):
    tokens = 0

    pX += conversion_error
    pY += conversion_error

    # Solve for a and b as before
    a = round((pY / bY - pX / bX) / (aY / bY - aX / bX))
    b = round((pX - a * aX) / bX)

    # Validate the solution
    if a * aX + b * bX == pX and a * aY + b * bY == pY:
        tokens += 3 * a + b

    return tokens


def common(fpath: PathLike) -> Tuple[int, int]:
    data = open(fpath).read().strip().split("\n\n")
    p1 = []
    p2 = []
    for machine in data:
        button_a, button_b, prize = machine.split("\n")

        aX, aY = map(int, re.findall(r"(\d+)", button_a))
        bX, bY = map(int, re.findall(r"(\d+)", button_b))
        pX, pY = map(int, re.findall(r"(\d+)", prize))

        p1_tokens = solve(aX, aY, bX, bY, pX, pY)
        if p1_tokens:
            p1.append(p1_tokens)

        p2_tokens = solve(aX, aY, bX, bY, pX, pY, 10000000000000)
        if p2_tokens:
            p2.append(p2_tokens)
    return (sum(p1), sum(p2))


def part1(fpath: PathLike) -> int:
    """Calculate the total cost for all claw machines."""
    return common(fpath)[0]


def part2(fpath: PathLike, debug: bool = False) -> int:
    return common(fpath)[1]


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
    # kw = {"debug": debug}
    kw = {}

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


# # Parsing function
# def parse_line(line: str, pattern: str) -> Tuple[int, int]:
#     """Generalized parser to extract the X, Y values from the line using regex"""
#     match = re.search(pattern, line)
#     if not match:
#         raise ValueError(f"Error parsing line {line}")
#     return int(match.group(1)), int(match.group(2))
#
#
# def parse_claw_machine_specs(
#     fpath: PathLike,
# ) -> List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
#     """Parse the machine specifications from the input file."""
#     machines = []
#     patterns = {
#         "a": r"Button A\: X\+(\d+), Y\+(\d+)",
#         "b": r"Button B\: X\+(\d+), Y\+(\d+)",
#         "c": r"Prize\:\W+X\=(\d+),\W+Y=(\d+),?",
#     }
#
#     with open(fpath, "r") as f:
#         while True:
#             # Read the three lines for each machine (skip empty lines)
#             line_a = f.readline().strip()
#             line_b = f.readline().strip()
#             line_c = f.readline().strip()
#
#             # If any of the lines are empty, break the loop (end of input)
#             if not line_a or not line_b or not line_c:
#                 break
#
#             # Parse Button A, Button B, and Prize positions
#             a = parse_line(line_a, patterns["a"])
#             b = parse_line(line_b, patterns["b"])
#             c = parse_line(line_c, patterns["c"])
#
#             # Add the parsed machine to the list
#             machines.append((a, b, c))
#
#             # Skip blank line (if any) after each machine specification
#             f.readline()  # This reads and discards the blank line
#
#     return machines
#
#
# # Calculation functions
# def calculate_vector_moves(
#     a: Tuple[int, int], b: Tuple[int, int], prize: Tuple[int, int]
# ) -> Tuple[int, int]:
#     """Solve for the move values (x and y) based on the system of equations"""
#     A, B = a
#     C, D = b
#     prize_x, prize_y = prize
#
#     # Constructing the system of equations:
#     # A*x + B*y = prize_x
#     # C*x + D*y = prize_y
#     # We can solve this using a determinant check for solvability
#
#     det = A * D - B * C  # The determinant of the system
#     if det == 0:
#         return 0, 0  # No solution, return zeros
#
#     # Calculate x and y using Cramer's rule
#     x = (prize_x * D - B * prize_y) / det
#     y = (A * prize_y - prize_x * C) / det
#
#     # Check if both x and y are integers
#     if x.is_integer() and y.is_integer():
#         return int(x), int(y)
#     else:
#         return 0, 0  # Return zeros if not valid
#
#
# def calculate_move_cost(x: int, y: int) -> int:
#     """Calculate the cost of a move, if valid"""
#     if x == 0 and y == 0:
#         return 0
#     return 3 * x + 1 * y  # Cost for A is 3, for B is 1
#
#
# # NOTE: 31571 is too low
# def part1(fpath: PathLike) -> int:
#     """Calculate the total cost for all claw machines."""
#     machines = parse_claw_machine_specs(fpath)
#     total_cost = 0
#     total_prizes = 0
#
#     for a, b, prize in machines:
#         x, y = calculate_vector_moves(a, b, prize)
#         print(f"Moves: {x}, {y}")
#         if x != 0 and y != 0:
#             total_cost += calculate_move_cost(x, y)
#             total_prizes += 1
#
#     return total_cost

# def parse_a(line: str) -> Tuple[int, int]:
#     match = re.search(r"Button A\: X\+(\d+), Y\+(\d+)", line)
#     if not match:
#         raise ValueError(f"Error parsing line {line}")
#     return int(match.group(1)), int(match.group(2))
#
#
# def parse_b(line: str):
#     match = re.search(r"Button B\: X\+(\d+), Y\+(\d+)", line)
#     if not match:
#         raise ValueError(f"Error parsing line {line}")
#     return int(match.group(1)), int(match.group(2))
#
#
# def parse_c(line: str):
#     match = re.search(r"Prize\:\W+X\=(\d+),\W+Y=(\d+),?", line)
#     if not match:
#         raise ValueError(f"Error parsing line {line}")
#     return int(match.group(1)), int(match.group(2))


# TODO: Try optimizing with asyncio to compute while reading
# def parse_claw_machine_specs(fpath: PathLike, debug: bool = False) -> np.ndarray:
#     machines = []
#     vectors = np.zeros((2, 3))
#     line_count = 0
#     with open(fpath, "r") as f:
#         for line in f.readlines():
#             line_count += 1
#             if line_count % 4 == 1:
#                 vectors[0][0], vectors[1][0] = parse_a(line)
#             elif line_count % 4 == 2:
#                 vectors[0][1], vectors[1][1] = parse_b(line)
#             elif line_count % 4 == 3:
#                 vectors[0][2], vectors[1][2] = parse_c(line)
#             else:
#                 machines.append(vectors.copy())
#                 if debug:
#                     print(machines[-1])
#                 continue
#     return np.array(machines)


# Calculation functions
# def calculate_vector_moves(machine: np.ndarray) -> np.ndarray:
#     vector, target = machine[:, :2], machine[:, 2]
#     if np.linalg.det(vector) == 0:
#         return np.zeros((1, 2), dtype=int)  # Return zeros if no solution
#     moves = np.linalg.solve(vector, target)
#     # Check if moves are integers
#     return (
#         moves if np.allclose(moves, moves.astype(int)) else np.zeros((1, 2), dtype=int)
#     )
#
#
# def calculate_move_cost(moves: np.ndarray) -> int:
#     # If no solution, cost is 0
#     if not moves.any():
#         return 0
#     # Otherwise, compute cost
#     return int(moves[0]) * 3 + int(moves[1]) * 2


# TODO: Try multiprocessing to split up each machine solution into worker thread
# def part1(fpath: PathLike, debug: bool = False) -> int:
#     machines = parse_claw_machine_specs(fpath, debug=debug)
#     costs = []
#     for machine in machines:
#         moves = calculate_vector_moves(machine)
#         cost = calculate_move_cost(moves)
#         costs.append(cost)
#         if debug:
#             print(f"Machine: \n{machine}\nMoves: {moves}\nCost: {cost}")
#     return sum(costs)
