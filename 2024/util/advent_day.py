import attrs
import datetime
from jinja2 import Environment, FileSystemLoader
import pathlib
from pathlib import Path

from util.sols import cprint

# TODO: Use rich.traceback to make errors more readable


@attrs.define
class AdventDay:
    URL_BASE = "https://adventofcode.com"
    PATH_UTIL = Path(__file__).parent
    PATH_AOC = PATH_UTIL.parent.parent
    PATH_TEMP = PATH_AOC / "templates"
    FILE_EX = "example.txt"
    FILE_IN = "input.txt"
    FILE_RM = "README.md"
    FILE_SL = "solve.py"

    _TODAY = datetime.date.today()
    _YR = _TODAY.year if _TODAY.month == 12 else _TODAY.year
    num: int = attrs.field(
        validator=[
            attrs.validators.instance_of(int),
            attrs.validators.ge(1),
            attrs.validators.le(25),
        ],
        kw_only=False,
    )
    title: str = attrs.field(default="", kw_only=False)
    year: int = attrs.field(default=_YR, kw_only=False)

    @property
    def str_num(self) -> str:
        return f"{self.num:02d}"

    @property
    def url(self) -> str:
        return f"{self.URL_BASE}/{self.year}/day/{self.num}"

    @property
    def url_input(self) -> str:
        return f"{self.url}/input"

    @property
    def path_yr(self) -> pathlib.Path:
        return self.PATH_AOC / str(self.year)

    @property
    def path_day(self) -> pathlib.Path:
        return self.path_yr / self.str_num

    @property
    def path_templates_dir(self) -> pathlib.Path:
        return self.path_yr / "templates"

    @property
    def path_example(self) -> pathlib.Path:
        return self.path_day / self.FILE_EX

    @property
    def path_input(self) -> pathlib.Path:
        return self.path_day / self.FILE_IN

    @property
    def path_readme(self) -> pathlib.Path:
        return self.path_day / self.FILE_RM

    @property
    def path_solve(self) -> pathlib.Path:
        return self.path_day / self.FILE_SL

    @property
    def context(self) -> dict[str, str]:
        return {
            "day_num": self.str_num,
            "day_str": self.str_num,
            "day_title": self.title,
            "day_url": self.url,
            "day_url_input": self.url_input,
            "URL_BASE": f"{self.URL_BASE}/{self.year}",
        }

    def mkdir(self) -> None:
        self.path_day.mkdir(parents=True, exist_ok=True)

    def render_tamplate(self, template_name: str, out_path: Path) -> None:
        env = Environment(loader=FileSystemLoader(self.path_templates_dir))
        templ = env.get_template(template_name)
        content = templ.render(self.context)
        # print(f"\nContent for {template_name}:\n{content}\n")
        with open(out_path, "w") as f:
            f.write(content)

    def render_example(self) -> None:
        self.render_tamplate("example.txt", self.path_example)

    def render_input(self) -> None:
        self.render_tamplate("input.txt", self.path_input)

    def render_readme(self) -> None:
        self.render_tamplate("README.md", self.path_readme)

    def render_solve(self) -> None:
        self.render_tamplate("solve.py", self.path_solve)

    def __str__(self) -> str:
        s = "AdventDay(\n"
        s += f"\tyear={self.year},\n"
        s += f"\tnum={self.num},\n"
        s += f"\ttitle={self.title},\n"
        s += f"\taoc_root={self.PATH_AOC},\n"
        s += f"\tdir_yr={self.path_yr},\n"
        s += f"\tdir_day={self.path_day},\n"
        s += f"\ttmpl={self.path_templates_dir},\n"
        s += f"\texa={self.path_example},\n"
        s += f"\tinp={self.path_input},\n"
        s += f"\trme={self.path_readme},\n"
        s += f"\tslv={self.path_solve},\n"
        s += f"\turl={self.url})"
        return s
