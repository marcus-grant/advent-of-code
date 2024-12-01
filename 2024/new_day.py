import attrs
import argparse
import os
from jinja2 import Environment, FileSystemLoader

PATH_PAR = os.path.dirname(os.path.realpath(__file__))
PATH_TEMP = os.path.join(PATH_PAR, 'templates')
URL_BASE = "https://adventofcode.com/2023"
FILE_EX = "example.txt"
FILE_IN = "input.txt"
FILE_RM = "README.md"
FILE_SL = "solve.py"

@attrs.define
class DayFacts:
    # Days are ints that are validated to be between 1~25
    num: int = attrs.field(
        validator=[
            attrs.validators.instance_of(int),
            attrs.validators.ge(1),
            attrs.validators.le(25)],
        kw_only=False)
    title: str = attrs.field(default='', kw_only=False)
    @property
    def str(self) -> str:
        return f"{self.num:02d}"
    @property
    def url(self) -> str:
        return f"{URL_BASE}/day/{self.num}"
    @property
    def url_input(self) -> str:
        return f"{URL_BASE}/day/{self.num}/input"
    @property
    def path_dir(self) -> os.PathLike:
        return os.path.join(PATH_PAR, self.str)
    @property
    def path_example(self) -> os.PathLike:
        return os.path.join(self.path_dir, FILE_EX)
    @property
    def path_input(self) -> os.PathLike:
        return os.path.join(self.path_dir, FILE_IN)
    @property
    def path_readme(self) -> os.PathLike:
        return os.path.join(self.path_dir, FILE_RM)
    @property
    def path_solve(self) -> os.PathLike:
        return os.path.join(self.path_dir, FILE_SL)
    @property
    def context(self) -> dict:
        return {
            'day_num': self.num,
            'day_str': self.str,
            'day_title': self.title,
            'day_url': self.url,
            'day_url_input': self.url_input,
            'URL_BASE': URL_BASE,
        }
    
    def make_dir(self) -> None:
        os.makedirs(self.path_dir, exist_ok=True)

def render_template(template_name: str, context: dict, output_path: str) -> None:
    env = Environment(loader=FileSystemLoader(PATH_TEMP))
    template = env.get_template(template_name)
    rendered_content = template.render(context)
    with open(output_path, 'w') as output_file:
        output_file.write(rendered_content)

def main(day: DayFacts) -> None:
    day.make_dir()
    render_template(FILE_EX, day.context, day.path_example)
    render_template(FILE_IN, day.context, day.path_input)
    render_template(FILE_RM, day.context, day.path_readme)
    render_template(FILE_SL, day.context, day.path_solve)

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
    main(DayFacts(args.day, args.title))
