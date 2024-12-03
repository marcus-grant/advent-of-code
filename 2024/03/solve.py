import re
from rich.markup import escape
from typing import List, Tuple

from util.sols import cprint


def read_lines(fpath: str) -> List[str]:
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
        filter_perc = (1 - (len(do_blocks) / len(instructions))) * 100
        msg = f"Filtered out {filter_perc:.2f}% of instructions"
        cprint(msg, style="bold blue")

    return do_blocks


def part1(fpath: str, debug: bool = False) -> int:
    darg = {"debug": debug}
    lines = read_lines(fpath)

    # The instructions need to be one long line this time
    instructions = "".join(lines)

    # Parse out the mul(X,Y) operands from the instructions
    muls = parse_mul_ops(instructions, **darg)
    total = sum(x * y for x, y in muls)

    return total


def part2(fpath: str, debug: bool = False) -> int:
    darg = {"debug": debug}
    lines = read_lines(fpath)
    instructions = "".join(lines)

    instructions = filter_dont_blocks(instructions, **darg)

    muls = parse_mul_ops(instructions, **darg)
    total = sum(x * y for x, y in muls)

    return total


if __name__ == "__main__":
    cprint(part1("input.txt"))
    cprint(part2("input.txt"))
