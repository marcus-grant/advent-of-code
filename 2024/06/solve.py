from enum import Enum
import pathlib
import time
from typing import Union, List, Tuple, Set, Optional
from rich.console import Console
import sys
from concurrent.futures import ProcessPoolExecutor
import os

console = Console()
cprint = console.print

DAY: str = "06"
TITLE: str = "Guard Gallivant"
COMMENTS: str = """Cleaner version without early exit heuristics"""

PathLike = Union[str, pathlib.Path]
Position = Tuple[int, int]
PositionSet = Set[Position]


def read_lines(fpath: PathLike) -> List[str]:
    """
    Read lines from a given file path.

    Args:
        fpath (PathLike): The file path to read from.

    Returns:
        List[str]: A list of lines from the file.
    """
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


class Direction(Enum):
    """
    Direction is an enumeration representing the four cardinal directions.
    """

    N = 0
    E = 1
    S = 2
    W = 3


class Grid:
    """
    Grid represents the environment in which the guard moves.
    It stores obstacle positions, dimensions, and can print a portion of the grid.
    """

    def __init__(self, lines: List[str], print_size: Position = (16, 32)):
        """
        Initialize the Grid.

        Args:
            lines (List[str]): The lines representing the grid.
            print_size (Position): The vertical and horizontal print boundary sizes.
        """
        self.lines = lines
        self.print_height = print_size[0]
        self.print_width = print_size[1]
        self.grid_height = len(lines)
        self.grid_width = len(lines[0])
        self.pos_obstacles = self._parse_char_positions(lines)

        if not all(len(line) == self.grid_width for line in lines):
            raise ValueError("All lines should have the same width.")

    def _parse_char_positions(self, lines: List[str], char: str = "#") -> PositionSet:
        """
        Parse obstacle positions from input lines.

        Args:
            lines (List[str]): The grid lines.
            char (str): The character representing an obstacle.

        Returns:
            PositionSet: A set of coordinates (r, c) where obstacles are located.
        """
        grid = set()
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch == char:
                    grid.add((r, c))
        return grid

    def inside(self, pos: Position) -> bool:
        """
        Check if a position is inside the grid.

        Args:
            pos (Position): The position to check.

        Returns:
            bool: True if inside the grid, False otherwise.
        """
        return 0 <= pos[0] < self.grid_height and 0 <= pos[1] < self.grid_width

    # TODO: Could use improvement
    def cprint(self, marker: Position, dir: Direction, visited: PositionSet) -> None:
        """
        Print a portion of the grid around the marker, ensuring a stable window size.

        This method prints a region of the grid centered on the marker with the dimensions:
        (2 * print_height + 1) rows by (2 * print_width + 1) columns.
        If the marker is near the edge, the window shifts so it remains within the grid.
        """
        # Desired dimensions
        total_height = 2 * self.print_height + 1
        total_width = 2 * self.print_width + 1

        # Compute the ideal top-left corner to center on the marker
        top = marker[0] - self.print_height
        left = marker[1] - self.print_width

        # Adjust if going out of the grid bounds vertically
        if top < 0:
            top = 0
        elif top + total_height > self.grid_height:
            top = max(self.grid_height - total_height, 0)

        # Adjust if going out of the grid bounds horizontally
        if left < 0:
            left = 0
        elif left + total_width > self.grid_width:
            left = max(self.grid_width - total_width, 0)

        # Now we have a stable window [top:top+total_height, left:left+total_width]
        direction_markers = ["^", ">", "v", "<"]

        for r in range(top, top + total_height):
            line_chars = []
            for c in range(left, left + total_width):
                if (r, c) in self.pos_obstacles:
                    line_chars.append(("#", "red"))
                elif (r, c) == marker:
                    m = direction_markers[dir.value]
                    line_chars.append((m, "bold green"))
                else:
                    if (r, c) in visited:
                        line_chars.append(("x", "color(8)"))
                    else:
                        line_chars.append((".", "color(8)"))
            for ch, style in line_chars:
                cprint(ch, end="", style=style)
            cprint("")


class Guard:
    """
    Guard represents the entity moving on the grid.
    It has a position and a direction, and can move forward or turn.
    """

    def __init__(self, position: Position, direction: Direction):
        """
        Initialize the Guard.

        Args:
            position (Position): The starting position of the guard.
            direction (Direction): The starting direction of the guard.
        """
        self.position = position
        self.direction = direction

    @classmethod
    def _parse_marker(cls, lines: List[str]) -> Tuple[Position, Direction]:
        """
        Parse the guard's starting position and direction from the input lines.

        Args:
            lines (List[str]): The grid lines.

        Returns:
            Tuple[Position, Direction]: The guard's starting position and direction.
        """
        n, e, s, w = Direction.N, Direction.E, Direction.S, Direction.W
        markers = {"^": n, ">": e, "v": s, "<": w}
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch in markers:
                    return (r, c), markers[ch]
        raise ValueError("No marker found in the grid.")

    def turn(self) -> None:
        """
        Turn the guard 90 degrees to the right.
        """
        self.direction = Direction((self.direction.value + 1) % 4)

    def forward_pos(self) -> Position:
        """
        Get the position in front of the guard based on its current direction.

        Returns:
            Position: The next position if the guard moves forward.
        """
        if self.direction == Direction.N:
            return (self.position[0] - 1, self.position[1])
        elif self.direction == Direction.E:
            return (self.position[0], self.position[1] + 1)
        elif self.direction == Direction.S:
            return (self.position[0] + 1, self.position[1])
        elif self.direction == Direction.W:
            return (self.position[0], self.position[1] - 1)
        else:
            raise ValueError("Invalid direction.")

    def move_forward(self):
        """
        Move the guard one step forward in its current direction.
        """
        self.position = self.forward_pos()


class Simulator:
    """
    Simulator runs the guard's movement on the given grid until either:
    - The guard leaves the grid
    - A loop in guard states (position, direction) is detected
    - The maximum step count is reached

    If record_positions is True, all visited cells are recorded.
    """

    def __init__(
        self,
        grid: Grid,
        guard: Guard,
        max_steps: int = 10**6,
        record_positions: bool = False,
    ) -> None:
        """
        Initialize the simulator.

        Args:
            grid (Grid): The grid on which the guard moves.
            guard (Guard): The guard to simulate.
            max_steps (int): Maximum steps to simulate before giving up.
            record_positions (bool): If True, record all visited cells.
        """
        self.grid: Grid = grid
        self.guard: Guard = guard
        self.max_steps: int = max_steps
        self.record_positions: bool = record_positions

        # Set of encountered guard states, each state is (position, direction)
        self.encountered_states: Set[Tuple[Position, Direction]] = set()

        # If recording positions, initialize a set to store visited cells
        self.visited_cells: Optional[Set[Position]] = (
            set() if record_positions else None
        )
        if self.visited_cells is not None:
            self.visited_cells.add(self.guard.position)

    def run(self) -> Tuple[bool, Set[Position]]:
        """
        Run the simulation until the guard leaves the grid or a loop is detected.

        Returns:
            Tuple[bool, Set[Position]]:
                loop_detected: True if a loop is found, False otherwise.
                visited_positions: The set of visited cells if record_positions is True,
                                   otherwise an empty set.
        """
        steps = 0
        self.encountered_states.add((self.guard.position, self.guard.direction))

        while self.grid.inside(self.guard.position) and steps < self.max_steps:
            next_pos = self.guard.forward_pos()

            if self.grid.inside(next_pos):
                if next_pos in self.grid.pos_obstacles:
                    self.guard.turn()
                else:
                    self.guard.move_forward()
                    if self.visited_cells is not None:
                        self.visited_cells.add(self.guard.position)
            else:
                # Guard leaves the grid
                return (
                    False,
                    self.visited_cells if self.visited_cells is not None else set(),
                )

            steps += 1

            current_state = (self.guard.position, self.guard.direction)
            if current_state in self.encountered_states:
                # Loop detected
                return (
                    True,
                    self.visited_cells if self.visited_cells is not None else set(),
                )
            else:
                self.encountered_states.add(current_state)

        # No loop detected and guard didn't leave (maybe max_steps reached)
        return (False, self.visited_cells if self.visited_cells is not None else set())


def record_path(path: List[Position], pos_marker: Position) -> List[Position]:
    """
    Record intermediate positions between the last recorded and the new pos_marker.

    This function is not currently used but provided for reference.

    Args:
        path (List[Position]): The current recorded path.
        pos_marker (Position): The new position of the marker.

    Returns:
        List[Position]: The updated path with intermediate positions included.
    """
    if len(path) == 0:
        path.append(pos_marker)
        return path

    last = path[-1]
    drow = pos_marker[0] - last[0]
    dcol = pos_marker[1] - last[1]

    if drow == 0 and dcol == 0:
        return path

    if drow != 0 and dcol != 0:
        raise ValueError("Marker moved diagonally, which should not happen.")

    if drow != 0:
        step = 1 if drow > 0 else -1
        for _ in range(abs(drow)):
            curr = path[-1]
            new_pos = (curr[0] + step, curr[1])
            path.append(new_pos)
    elif dcol != 0:
        step = 1 if dcol > 0 else -1
        for _ in range(abs(dcol)):
            curr = path[-1]
            new_pos = (curr[0], curr[1] + step)
            path.append(new_pos)

    return path


def part1(fpath: PathLike, debug: bool = False) -> int:
    """
    Solve part 1 of the puzzle.

    Args:
        fpath (PathLike): The path to the input file.
        debug (bool): If True, prints debugging information whenever the guard hits an obstacle.

    Returns:
        int: The count of visited distinct positions by the guard before leaving the grid.
    """
    lines = read_lines(fpath)
    grid = Grid(lines)
    guard_start_pos, guard_start_dir = Guard._parse_marker(lines)
    guard = Guard(guard_start_pos, guard_start_dir)

    sim = Simulator(grid, guard, max_steps=10**6, record_positions=True)

    loop_found = False
    sim.encountered_states.add((guard.position, guard.direction))

    while grid.inside(guard.position) and len(sim.encountered_states) < sim.max_steps:
        next_pos = guard.forward_pos()

        if grid.inside(next_pos):
            if next_pos in grid.pos_obstacles:
                # Obstacle ahead, turn right
                guard.turn()
                if debug:
                    cprint("[DEBUG] Hit obstacle and turned right:")
                    grid.cprint(
                        guard.position, guard.direction, sim.visited_cells or set()
                    )
            else:
                # Move forward
                guard.move_forward()
                if sim.visited_cells is not None:
                    sim.visited_cells.add(guard.position)
        else:
            # Guard leaves the grid
            break

        current_state = (guard.position, guard.direction)
        if current_state in sim.encountered_states:
            loop_found = True
            break
        sim.encountered_states.add(current_state)

    return len(sim.visited_cells) if sim.visited_cells is not None else 0


def test_candidate(
    candidate: Position,
    grid: Grid,
    guard_pos: Position,
    guard_dir: Direction,
    max_steps: int = 10**6,
) -> bool:
    """
    Test if placing an obstruction at the candidate position causes a loop.

    Args:
        candidate (Position): The position to place the new obstruction.
        grid (Grid): The grid in which the guard moves.
        guard_pos (Position): The guard's starting position.
        guard_dir (Direction): The guard's starting direction.
        max_steps (int): Maximum number of steps to simulate.

    Returns:
        bool: True if a loop is detected, False otherwise.
    """
    grid.pos_obstacles.add(candidate)
    guard = Guard(guard_pos, guard_dir)
    sim = Simulator(grid, guard, max_steps=max_steps)
    loop_found, _ = sim.run()
    grid.pos_obstacles.remove(candidate)
    return loop_found


def run_candidate(args: Tuple[Position, List[str], Position, Direction]) -> bool:
    """
    Wrapper function to rebuild the grid and test a candidate obstruction.

    Args:
        args (Tuple[Position, List[str], Position, Direction]):
            candidate: The candidate obstruction position.
            lines: The grid lines.
            guard_start_pos: The guard's start position.
            guard_start_dir: The guard's start direction.

    Returns:
        bool: True if a loop is detected by placing the candidate obstruction.
    """
    candidate, lines, guard_start_pos, guard_start_dir = args
    test_grid = Grid(lines)
    return test_candidate(candidate, test_grid, guard_start_pos, guard_start_dir)


def part2(fpath: PathLike, debug: bool = False) -> int:
    """
    Solve part 2 of the puzzle.

    Args:
        fpath (PathLike): The path to the input file.
        debug (bool): If True, prints a message but won't debug for large input due to performance.

    Returns:
        int: The count of positions where placing a new obstruction leads to a loop.
    """
    # If debugging is enabled but this is the real input, we won't debug due to performance.
    if debug and "input.txt" in str(fpath):
        print("\nDebugging disabled on this part due to performance issues.\n")

    lines = read_lines(fpath)
    grid = Grid(lines)
    guard_start_pos, guard_start_dir = Guard._parse_marker(lines)

    candidates = [
        (r, c)
        for r in range(grid.grid_height)
        for c in range(grid.grid_width)
        if (r, c) not in grid.pos_obstacles and (r, c) != guard_start_pos
    ]

    tasks = [
        (candidate, lines, guard_start_pos, guard_start_dir) for candidate in candidates
    ]

    loop_count = 0
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for result in executor.map(run_candidate, tasks):
            if result:
                loop_count += 1

    return loop_count


def bgrn(s) -> str:
    """
    Return a string formatted in green and bold.

    Args:
        s (str): The string to format.

    Returns:
        str: The formatted string.
    """
    return f"\033[1;32m{s}\033[0m"


def mgta(s) -> str:
    """
    Return a string formatted in magenta.

    Args:
        s (str): The string to format.

    Returns:
        str: The formatted string.
    """
    return f"\033[35m{s}\033[0m"


def blue(s) -> str:
    """
    Return a string formatted in blue.

    Args:
        s (str): The string to format.

    Returns:
        str: The formatted string.
    """
    return f"\033[34m{s}\033[0m"


def run(debug: bool = False) -> None:
    """
    Run both parts of the puzzle solution, printing results and timings.

    Args:
        debug (bool): If True, enable debugging prints in part1 and a note in part2.
    """
    PATH_EX = pathlib.Path(__file__).parent / "example.txt"
    PATH_IN = pathlib.Path(__file__).parent / "input.txt"
    kw = {"debug": debug}

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
    debug = any(arg in {"--debug", "-d"} for arg in sys.argv)
    run(debug)
