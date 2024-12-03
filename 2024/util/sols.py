# util/sols.py
import importlib.util
import os
import sys
import traceback
from rich.console import Console
from rich.panel import Panel

from typing import Literal, Optional, Callable, Any

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
        justify (Literal["left", "center", "right"], optional): Text justification. Defaults to "center".
    """
    panel_title = title if title else None
    panel = Panel.fit(msg, title=panel_title, style=style)
    cprint(panel, justify=justify, new_line_start=True)


def read_lines(fpath: str) -> list[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def dynamic_import(day: str) -> Optional[object]:
    """
    Dynamically imports the solve.py module from the given day directory.

    Args:
        day (str): The day directory name (e.g., '01').

    Returns:
        module: The imported solve.py module, or None if import fails.
    """
    module_name = f"day_{day}"
    # Get the absolute path to the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    module_path = os.path.join(current_dir, "..", day, "solve.py")  # Adjusted path

    # Normalize the path
    module_path = os.path.normpath(module_path)

    if not os.path.exists(module_path):
        console.print(
            f"[bold red]'solve.py' not found in directory '{day}'.[/bold red]"
        )
        return None

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        console.print(
            f"[bold red]Could not load spec for module '{module_name}'.[/bold red]"
        )
        return None

    if spec.loader is None:
        console.print(
            f"[bold red]Spec loader is None for module '{module_name}'.[/bold red]"
        )
        return None

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        console.print(
            f"[bold red]Error importing module '{module_name}': {e}[/bold red]"
        )
        traceback.print_exc()
        return None

    return module


def execute_part(
    part_func: Callable[[Any, bool], int], fpath: str, debug: bool = False
) -> Optional[Any]:
    """
    Executes a part function and handles exceptions.

    Args:
        part_func (callable): The part1 or part2 function to execute.
        fpath (str): The path to the input file.

    Returns:
        The result of the part function, or None if an error occurred.
    """
    try:
        if debug:
            return part_func(fpath, debug=True)  # type: ignore
        else:
            return part_func(fpath)  # type: ignore
    except Exception as e:
        console.print(f"[bold red]Error executing {part_func.__name__}: {e}[/bold red]")
        traceback.print_exc()
        return None
