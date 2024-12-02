import attrs
import argparse
import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict

# Constants
URL_BASE = "https://adventofcode.com"
FILE_EX = "example.txt"
FILE_IN = "input.txt"
FILE_RM = "README.md"
FILE_SL = "solve.py"

# TODO: Automate making solve.py executable
# TODO: Add rich console
# Init rich console
# console = Console()
# cprint = console.print

# Paths
PATH_PAR = Path(__file__).parent
PATH_TEMP = PATH_PAR / "templates"


def default_year() -> int:
    """
    Determine the default year.
    - If month is December, it's the current year
    - Otherwise, use previous year
    """
    today = datetime.date.today()
    return today.year if today.month == 12 else today.year - 1


@attrs.define
class DayFacts:
    # Days are ints that are validated to be between 1~25 (inclusive)
    # TODO: Add year that defaults to last year unless it's December
    num: int = attrs.field(
        validator=[
            attrs.validators.instance_of(int),
            attrs.validators.ge(1),
            attrs.validators.le(25),
        ],
        kw_only=False,
    )
    title: str = attrs.field(default="", kw_only=False)
    year: int = attrs.field(default=default_year(), kw_only=False)

    @property
    def str_num(self) -> str:
        return f"{self.num:02d}"

    @property
    def url(self) -> str:
        return f"{URL_BASE}/{self.year}/day/{self.num}"

    @property
    def url_input(self) -> str:
        return f"{URL_BASE}/{self.year}/day/{self.num}/input"

    @property
    def path_dir(self) -> Path:
        return PATH_PAR / self.str_num

    @property
    def path_example(self) -> Path:
        return self.path_dir / FILE_EX

    @property
    def path_input(self) -> Path:
        return self.path_dir / FILE_IN

    @property
    def path_readme(self) -> Path:
        return self.path_dir / FILE_RM

    @property
    def path_solve(self) -> Path:
        return self.path_dir / FILE_SL

    @property
    def context(self) -> dict[str, str]:
        return {
            "day_num": self.str_num,
            "day_str": self.str_num,
            "day_title": self.title,
            "day_url": self.url,
            "day_url_input": self.url_input,
            "URL_BASE": f"{URL_BASE}/{self.year}",
        }

    def make_dir(self) -> None:
        self.path_dir.mkdir(parents=True, exist_ok=True)


def render_template(
    template_name: str, context: Dict[str, str], output_path: Path
) -> None:
    env = Environment(loader=FileSystemLoader(PATH_TEMP))
    template = env.get_template(template_name)
    rendered_content = template.render(context)
    with open(output_path, "w") as output_file:
        output_file.write(rendered_content)


def main(day: DayFacts) -> None:
    day.make_dir()
    render_template(FILE_EX, day.context, day.path_example)
    render_template(FILE_IN, day.context, day.path_input)
    render_template(FILE_RM, day.context, day.path_readme)
    render_template(FILE_SL, day.context, day.path_solve)


if __name__ == "__main__":
    parser_desc = "Templating script to create the dir/files needed to "
    parser_desc += "complete a day of the advent of code"
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument("day", type=int, help="The day of advent (between 1~25)")
    parser.add_argument("title", type=str, help="The day of advent story title")
    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=default_year(),
        help="Year of Advent of Code (defaults to last year unless it's Dec.)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Don't print debug lines of anything to the console",
    )
    args = parser.parse_args()
    main(DayFacts(args.day, args.title, args.year))
