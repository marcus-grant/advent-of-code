import re
from rich.console import Console
from rich.panel import Panel
from rich import rule
from rich.markup import escape

from typing import List, Tuple, Literal

console = Console()
cprint = console.print


def print_solution(
    sol: str,
    title: str = "",
    style: str = "bold red",
    justify: Literal["center", "left", "right"] = "center",
) -> None:
    # Construct the title message with conditional formatting
    if title:
        msg = f"[bold green]Solution to {title}[/bold green]"
    else:
        msg = "[bold green]Solution[/bold green]"

    # Create a Rich Panel with the solution text
    panel = Panel.fit(
        sol,
        title=msg,
        style=style,
        border_style=style,
        padding=(1, 2),  # Optional: Adds padding for better aesthetics
    )
    # Print the panel with specified justification
    cprint(panel, justify=justify, new_line_start=True)


def print_panel(
    msg: str,
    title: str = "",
    style: str = "yellow",
    justify: Literal["left", "center", "right"] = "center",
) -> None:
    """
    Print a styled panel using Rich.

    Args:
        msg (str): The message to display inside the panel.
        title (str, optional): The title of the panel. Defaults to "".
        style (str, optional): The style of the panel. Defaults to "yellow".
        justify (Literal["left", "center", "right"], optional):
            Text justification. Defaults to "center".
    """
    panel_title = title if title else None
    panel = Panel.fit(msg, title=panel_title, style=style)
    cprint(panel, justify=justify, new_line_start=True)


def read_lines(fpath: str) -> list[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def if_debug_print(debug: bool, msg: str, esc: bool = False) -> None:
    msg = escape(msg) if esc else msg
    cprint(msg) if debug else None


def parse_mul_ops(line: str, debug: bool) -> List[Tuple[int, int]]:
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, line)
    ops = [(int(x), int(y)) for x, y in matches]

    if debug:
        cprint("\n[blue]mul operands[/blue]:\n")
        cprint(ops)
        cprint("\n[green]mul operands[/green]:\n")
        cprint(ops)
        cprint()

    return ops


def filter_dont_blocks(instructions: str, debug: bool) -> str:
    pattern = r"don't\(\).*?($|do\(\))"
    do_blocks = re.sub(pattern, "", instructions, flags=re.DOTALL)

    # Print debug info if requested
    if debug:
        cprint("\n[blue]instructions[/blue]:\n")
        cprint(escape(instructions))
        cprint("\n[green]do_blocks[/green]:\n")
        cprint(escape(do_blocks))
        cprint()

    return do_blocks


def part1(fpath: str, debug: bool) -> int:
    darg = {"debug": debug}
    lines = read_lines(fpath)

    # The instructions need to be one long line this time
    instructions = "".join(lines)

    # Parse out the mul(X,Y) operands from the instructions
    muls = parse_mul_ops(instructions, **darg)
    total = sum(x * y for x, y in muls)

    return total


def part2(fpath: str, debug: bool) -> int:
    darg = {"debug": debug}
    lines = read_lines(fpath)
    instructions = "".join(lines)

    instructions = filter_dont_blocks(instructions, **darg)

    muls = parse_mul_ops(instructions, **darg)
    total = sum(x * y for x, y in muls)

    return total


def main(day_str: str, d: bool) -> None:
    EXAMPLE = f"{day_str}/example.txt"
    EXAMPLE2 = f"{day_str}/example2.txt"
    INPUT = f"{day_str}/input.txt"
    TITLES = [  # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE",
        "Part One - INPUT",
        "Part Two - EXAMPLE",
        "Part Two - INPUT",
    ]
    for t in TITLES:
        print_panel(t, style="bold green")
        if "one" in t.lower() or "1" in t.lower():
            if "example" in t.lower():
                print_solution(f"{part1(EXAMPLE, d)}", title=t)
                continue
            print_solution(f"{part1(INPUT, d)}", title=t)
            continue
        if "example" in t.lower():
            print_solution(f"{part2(EXAMPLE2, d)}", title=t)
            continue
        print_solution(f"{part2(INPUT, d)}", title=t)


if __name__ == "__main__":
    import argparse

    DAY = "03"
    DAY_TITLE = "Mull It Over"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Don't print debug lines of anything to the console",
    )
    args = parser.parse_args()
    # msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE}[/bold green]"
    cprint(rule.Rule(title=f"Advent of Code - Day {DAY} - {DAY_TITLE}"), style="red")
    # print_panel(msg ,style="bold red")
    main(DAY, args.debug)
    # msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]"
    # print_panel(msg, style="bold green")
    cprint(rule.Rule(title=f"Advent of Code - Day {DAY} - Complete!"), style="red")

