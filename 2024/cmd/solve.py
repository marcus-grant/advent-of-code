# cmd/solve.py
import argparse
import pathlib
from rich import rule
import sys

from typing import List, Callable

from util.sols import dynamic_import, execute_part
from util.sols import print_solution, cprint


def parser_factory() -> argparse.ArgumentParser:
    # Create a parser specific to the 'solve' subcommand
    parser = argparse.ArgumentParser(
        description="Solve a specific Advent of Code Day's problem"
    )

    # Define arguments for 'solve' subcommand
    parser.add_argument(
        "day", type=int, help="Day of the Advent of Code problem to solve (1-25)"
    )
    parser.add_argument(
        "--part",
        "-p",
        choices=["1", "2", "all"],
        default="all",
        help="Specify which part to solve (default: all)",
    )
    parser.add_argument(
        "--example",
        "-e",
        action="store_true",
        help="Whether to solve with example data (default: no)",
    )
    parser.add_argument(
        "--real",
        "-r",
        action="store_true",
        help="Whether to solve with real input data (default: no)",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Whether to print debug information (default: no)",
    )
    return parser


def parse_args(args):
    parser = parser_factory()  # Create parser
    args = parser.parse_args(args)  # Parse

    # Here we make some small adjustments to the parsed arguments
    # First zero pad the day number as a string
    args.day = f"{args.day:02d}"

    # If both example and real flags are unset, set both to True
    if not args.example and not args.real:
        args.example = True
        args.real = True

    # If parts are set to all then set to ["1", "2"]
    # Otherwise convert to a list of the single part
    if args.part == "all":
        args.part = ["1", "2"]
    else:
        args.part = [args.part]

    return args


SolverType = Callable[[str, bool], int]


def get_solvers(day: str, part: str) -> List[SolverType]:
    # Dynamically import the module for the specified day
    solver_module = dynamic_import(day)

    solvers = []  # Init the list of solvers
    # Check part 1 is requested and exists then add to solvers
    if "1" in part:
        if hasattr(solver_module, "part1"):
            solvers.append(getattr(solver_module, "part1", None))

    # Check part 2 is requested and exists then add to solvers
    if "2" in part:
        if hasattr(solver_module, "part2"):
            solvers.append(getattr(solver_module, "part2", None))

    # Filter out any None values from the getattr calls
    solvers = list(filter(None, solvers))

    return solvers


def main(args):
    args = parse_args(args)

    # Set day's title via dynamic import
    YEAR = str(2024)
    title = getattr(dynamic_import(args.day), "TITLE", None)
    title = title if title else "CANNOT FIND TITLE!!!"

    # Print the Title of the Day and solving prompt
    rule_title = f"Solving Advent of Code {YEAR} - Day {args.day} - {title}"

    # Get the solvers for the specified day and part
    solvers = get_solvers(args.day, args.part)

    # Print important variables for execution
    cprint("Arguments:", style="bold blue")
    cprint(args)
    cprint("Solvers:", style="bold blue")
    cprint(solvers)
    cprint(rule.Rule(title=rule_title), style="red")

    # Check if no solvers
    if solvers is None or len(solvers) == 0:
        msg = f"No solvers found for Day {args.day} - Part {args.part}"
        cprint(msg, style="bold red")
        sys.exit(1)
    # To make serial execution easier, duplicate solver
    if len(solvers) < 2 and "2" in args.part:
        solvers.append(solvers[0])

    # Calculate paths for solvers to use as input
    path_aoc = pathlib.Path(__file__).parent.parent
    path_real = path_aoc / args.day / "input.txt"
    path_real2 = path_aoc / args.day / "input2.txt"
    path_ex = path_aoc / args.day / "example.txt"
    path_ex2 = path_aoc / args.day / "example2.txt"
    sol1_ex, sol1_r, sol2_ex, sol2_r = None, None, None, None

    # If either example2.txt or input2.txt doesn't exist set to None
    if not path_ex2.exists():
        path_ex2 = path_ex
    if not path_real2.exists():
        path_real2 = path_real

    # First run the first part's solver with example data if requested
    # FIXME: Weird bug where if sol is 0 it thinks no solution found
    if args.example and "1" in args.part:
        sol1_ex = execute_part(solvers[0], path_ex, args.debug)
        sol1_ex = sol1_ex if isinstance(sol1_ex, int) else None
        # Print the solution for part if it exists
        if sol1_ex:
            print_solution(str(sol1_ex), title=f"Day {args.day} - Part 1 - EXAMPLE")
        else:
            msg = f"No solution found for Day {args.day} - Part 1 - EXAMPLE"
            cprint(msg, style="bold red")

    # Next run the first part's solver with real data if requested
    if args.real and "1" in args.part:
        sol1_r = execute_part(solvers[0], path_real, args.debug)
        sol1_r = sol1_r if isinstance(sol1_r, int) else None
        if sol1_r:
            print_solution(str(sol1_r), title=f"Day {args.day} - Part 1 - INPUT")
        else:
            msg = f"No solution found for Day {args.day} - Part 1 - INPUT"
            cprint(msg, style="bold red")

    # Next run the second part's solver with example data if requested
    if args.example and "2" in args.part:
        sol2_ex = execute_part(solvers[1], path_ex2, args.debug)
        sol2_ex = sol2_ex if isinstance(sol2_ex, int) else None
        if sol2_ex:
            print_solution(str(sol2_ex), title=f"Day {args.day} - Part 2 - EXAMPLE")
        else:
            msg = f"No solution found for Day {args.day} - Part 2 - EXAMPLE"
            cprint(msg, style="bold red")

    # Finally run the second part's solver with real data if requested
    if args.real and "2" in args.part:
        sol2_r = execute_part(solvers[1], path_real2, args.debug)
        sol2_r = sol2_r if isinstance(sol2_r, int) else None
        if sol2_r:
            print_solution(str(sol2_r), title=f"Day {args.day} - Part 2 - INPUT")
        else:
            msg = f"No solution found for Day {args.day} - Part 2 - INPUT"
            cprint(msg, style="bold red")
