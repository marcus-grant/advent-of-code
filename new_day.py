import os
import argparse

def create_day_dir(day: int) -> None:
    if not isinstance(day, int) or day < 1 or day > 25:
        raise ValueError(f"Invalid day. Day must be in between 1~25. Got {day}")

    dir_name = f"{day:02d}"
    os.makedirs(dir_name, exist_ok=True)

def create_readme(day: int, title: str) -> None:
    day_str = f"{day:02d}"
    content = f"# Day {day_str} - {title}\n\n"
    content += "## Part One\n\n"
    content += "TODO: Add example one description for Part One.\n\n"
    content += "```txt\n"
    content += "```\n\n"
    content += "## Part Two\n\n"
    content += "TODO: Add example two description for Part Two.\n\n"
    content += "```txt\n"
    content += "```\n\n"
    content += "## Links\n\n"
    content += '\n'
    content += f"- [Advent of Code - Calendar][aoc-calendar]\n"
    content += f"- [Advent of Code - Day {day_str}][aoc-day{day}]\n"
    content += f"- [Advent of Code - Day {day_str} - Input][aoc-day{day}-input]\n"
    content += '\n'
    content += f"<!-- Hidden References -->\n"
    content += f"[aoc-calendar]: https://adventofcode.com/2023 \"Advent of Code - Calendar\"\n"
    content += f"[aoc-day{day}]: https://adventofcode.com/2023/day/{day} \"Advent of Code - Day {day_str}\"\n"
    content += f"[aoc-day{day}-input]: https://adventofcode.com/2023/day/{day}/input \"Advent of Code - Day {day_str} - Input\"\n"
    
    with open(f"{day_str}/README.md", "w") as readme_file:
        readme_file.write(content)
    
def create_solve(day: int, title: str = '') -> None:
    ss: list[str] = []
    ss.append('from attrs import asdict, define, make_class, Factory')
    ss.append('from dataclasses import dataclass, field')
    ss.append('from typing import List, Tuple')
    ss.append('from colorama import Fore, Back, Style')
    ss.append('from pprint import pprint')
    ss.append('from pydantic import BaseModel')
    ss.append('')
    ss.append('def print_solution(sol: str, title: str="' + title + '"):')
    ss.append('    s = f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.CYAN}Solution"')
    ss.append('    if len(title) > 0:')
    ss.append('        s += f" to {title}"')
    ss.append('    s += f"{Style.RESET_ALL}: {Back.LIGHTCYAN_EX}{Fore.BLACK}{sol}{Style.RESET_ALL}"')
    ss.append('    print(s)')
    ss.append('')
    ss.append('def read_input(input_file_path: str) -> list[str]:')
    ss.append('    with open(input_file_path, "r") as f:')
    ss.append('        lines = f.read().splitlines()')
    ss.append('    return lines')
    ss.append('')
    ss.append('def part1(input_file: str) -> int:')
    ss.append('    lines = read_input(input_file)')
    ss.append('    return 0')
    ss.append('')
    ss.append('def part2(input_file: str) -> int:')
    ss.append('    lines = read_input(input_file)')
    ss.append('    return 0')
    ss.append('')
    ss.append('def main():')
    ss.append('    EXAMPLE = "example.txt"')
    ss.append('    INPUT = "input.txt"')
    ss.append('')
    ss.append('    print()')
    ss.append('    print("Part One - Example")')
    ss.append('    print("==================")')
    ss.append('')
    ss.append('    print()')
    ss.append('    solution = part1(EXAMPLE)')
    ss.append('    print_solution(f"\\n{solution}\\n", title="Part One (Example)")')
    ss.append('')
    ss.append('    print()')
    ss.append('    print("Part One - Input")')
    ss.append('    print("=================")')
    ss.append('')
    ss.append('    print()')
    ss.append('    # TODO: Implement Part One Input')
    ss.append('')
    ss.append('    print()')
    ss.append('    print("Part Two - Example")')
    ss.append('    print("==================")')
    ss.append('')
    ss.append('    print()')
    ss.append('    # TODO: Implement Part Two Example')
    ss.append('')
    ss.append('    print()')
    ss.append('    print("Part Two - Input")')
    ss.append('    print("================")')
    ss.append('')
    ss.append('    print()')
    ss.append('    # TODO: Implement Part Two Input')
    ss.append('')
    ss.append('if __name__ == "__main__":')
    title = f" Day {day:02d} - {title} " 
    left_pad = (64 - len(title)) // 2
    right_pad = 64 - len(title) - left_pad
    left_pad = left_pad * "="
    right_pad = right_pad * "="
    ts = left_pad + title + right_pad
    ss.append(f"    print('{ts}')")
    ss.append('    main()')
    title = f" Day {day:02d} - Complete "
    left_pad = (64 - len(title)) // 2
    right_pad = 64 - len(title) - left_pad
    left_pad = left_pad * "="
    right_pad = right_pad * "="
    ts = left_pad + title + right_pad
    ss.append(f"    print('{ts}')")
    ss.append('')
    ss = [s + '\n' for s in ss]
    with open(f"{day:02d}/solve.py", "w") as solve_file:
        solve_file.writelines(ss)

    
# https://adventofcode.com/2023/day/3
def create_all_day_templates(day: int, title: str) -> None:
    if not isinstance(day, int) or day < 1 or day > 25:
        raise ValueError(f"Invalid day. Day must be in between 1~25. Got {day}")
    day_str = f"{day:02d}"
    print(f"Creating files & directories for Advent of Code!")
    print(f"Day {day_str} - {title}")
    print(f"First creating directory {day_str}")
    try:
        create_day_dir(day)
    except Exception as e:
        print(f"Error creating directory: {str(e)}")
    print("Done!")
    print(f"Creating README file for diary entry.")
    create_readme(day, title)
    print('Done!')
    print(f"Creating solve.py file for day {day_str}.")
    create_solve(day)
    print('Done!')

if __name__ == '__main__':
    parser_desc = 'Templating script to create the dir/files needed to '
    parser_desc += 'complete a day of the advent of code'
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument(
        'day',
        type=int,
        help='The day of advent (between 1~25)')
    parser.add_argument(
        'title',
        type=str,
        help='The day of advent story title')
    args = parser.parse_args()
    print(f"day: {args.day}, title: {args.title}")
    create_all_day_templates(args.day, args.title)
