import argparse
import datetime
import sys
from rich.rule import Rule

from util.advent_day import AdventDay
from util.sols import cprint


def parse_args(args):
    # Create parser
    desc = "Template & Download New Advent of Code Day"
    parser = argparse.ArgumentParser(description=desc)

    # Get year of current or last December
    today = datetime.date.today()
    year = today.year if today.month == 12 else today.year - 1

    # Define arguments for 'new' subcommand
    day_help = "Day of Advent of Code to template/download"
    parser.add_argument("day", type=int, help=day_help)
    parser.add_argument("title", type=str, help="Title of the day diary")
    year_help = "Year of Advent of Code (default: last/current December year"
    parser.add_argument("--year", "-y", type=int, default=year, help=year_help)
    debug_help = "Print debug info without taking action (default: False)"
    parser.add_argument("--debug", "-d", action="store_true", help=debug_help)
    parser.add_argument("--quiet", "-q", action="store_true", help="No stdout messages")

    # Parse
    args = parser.parse_args(args)
    return args


def main(args):
    args = parse_args(args)  # Parse CLI args
    day = AdventDay(num=args.day, title=args.title, year=args.year)

    # If debug flag is set
    if args.debug:
        # Print day attributes
        cprint(day, style="bold blue")
        cprint(str(day), style="bold magenta")
        sys.exit(0)

    if not args.quiet:
        rule_title = f"Year {day.year} - Day {day.str_num} - Title {day.title}"
        rule_sub = "Generating Advent of Code Files.."
        print()
        cprint(Rule(title=rule_title, style="bold green"), style="bold magenta")
        cprint(Rule(title=rule_sub, style="magenta"), style="")
        print()
        cprint(f"Making new day dir\t@\t{day.path_day}...", style="")
    day.mkdir()  # Init AdventDay w/ args & make year/day dir

    # Now render all the templates into the year/day dir

    if not args.quiet:
        cprint(f"Rendering example.txt\t@\t{day.path_day}...", style="")
    day.render_example()
    if not args.quiet:
        cprint(f"Rendering input.txt\t@\t{day.path_day}...", style="")
    day.render_input()
    if not args.quiet:
        cprint(f"Rendering README.md\t@\t{day.path_day}...", style="")
    day.render_readme()
    if not args.quiet:
        cprint(f"Rendering solve.py\t@\t{day.path_day}...", style="")
    day.render_solve()

    if not args.quiet:
        print()
        cprint(f"Open solver\t@\t{day.path_solve}", style="bold")
        cprint(f"Or Day URL \t@\t{day.url}", style="bold")
        print()
        rule_sub = "Advent of Code file generation complete!"
        rule_title = "Done!"
        print()
        cprint(Rule(title=rule_sub, style="magenta"), style="")
        cprint(Rule(title=rule_title, style="green"), style="bold")
        print()
