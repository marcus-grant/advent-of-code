from rich.console import Console
import time
from typing import List, Tuple, Set
# import numpy as np

console = Console()
cprint = console.print


# Solver ID Constants
DAY: str = "04"
TITLE: str = "Ceres Search"
TODO = """
This is an extremely rough solotion that needs cleaning up
I think it could work the old way but I lost time.
Should also see what numpy can do for performance
"""


def read_lines(fpath: str) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


Position = Tuple[int, int]
SetOfPositions = Set[Position]
WordCharPositions = List[SetOfPositions]
Vector = Tuple[int, int]
Vectors = List[Vector]


def find_char_positions(char: str, grid: List[str]) -> SetOfPositions:
    positions = set()
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == char:
                positions.add((r, c))
    return positions


def check_direction(
    word_char_positions: WordCharPositions, pos: Position, vec: Vector
) -> bool:
    for step in range(1, len(word_char_positions)):
        # Get the next char's positions set
        next_char_positions = word_char_positions[step]

        # Calculate the next position by multiplying the vector with step...
        # ...and adding that product to the given position
        pos_next = (vec[0] * step + pos[0], vec[1] * step + pos[1])

        # Check if the next position is in the next char's positions set
        if pos_next not in next_char_positions:
            # If not, then we know this direction is a dead end
            return False
    # If we exit the loop then we've checked all the chars in the word
    # From the given position and vector we have found the word
    return True


# NOTE: This is a quick and dirty helper method that works
def part1(fpath: str, debug: bool = False) -> int:
    grid = read_lines(fpath)

    # Compute adjacent vectors
    vectors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Exclude sine it's origin position
            vectors.append((i, j))

    # Find positions Set(r, c) of 'X', 'M', 'A', 'S' chars
    # Put that set of tuples representing positions into a list,
    # each representing chars in a word.
    # This way following dir vectors you multiply vector by index of char
    word_char_positions = [
        find_char_positions("X", grid),  # x_position * vector * 0 = x_position
        find_char_positions("M", grid),  # x_position * vector * 1 = m_position
        find_char_positions("A", grid),  # x_position * vector * 2 = a_position
        find_char_positions("S", grid),  # x_position * vector * 3 = s_position
    ]

    found_words = []
    for origin_position in word_char_positions[0]:
        for vector in vectors:
            if check_direction(word_char_positions, origin_position, vector):
                found_words.append(origin_position)

    found_word_count = len(found_words)
    return found_word_count


# NOTE: 18 correct for example, but 2062 too high for real data
# NOTE: 1024 too low (answer between 1024 and 2062)
# NOTE: 1536 too low (answer between 1536 and 2062)
# NOTE: 1792 wrong, 2006 wrong
# NOTE: Answer is 2003
def part2(fpath: str, debug: bool = False) -> int:
    grid = read_lines(fpath)

    # Setup timers to check performance
    tstart = time.time()

    # There's three letter positions we need for this version
    positions_m = find_char_positions("M", grid)
    positions_a = find_char_positions("A", grid)
    positions_s = find_char_positions("S", grid)

    # The A positions are the origin positions now
    # Every X shaped cross is centered about an 'A'
    # No matter the arrangements of M and S in the corners.
    # So use a list of vectors again, but for each corner from 'A'
    vectors = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

    # Now to iterate for every 'A' position and every vector from that position
    cross_positions = []
    for pos_a in positions_a:
        count_m = 0
        count_s = 0
        # if pos_a[0] == 123 and pos_a[1] == 75:
        #     breakpoint()
        for vec in vectors:
            # With this position and vector, calculate resulting corner position
            pos_corner = (pos_a[0] + vec[0], pos_a[1] + vec[1])
            # Check for 'M' and 'S and count them
            if pos_corner in positions_m:
                count_m += 1
            if pos_corner in positions_s:
                count_s += 1
        # Now we've counted M & S in corners of one A position
        # There should be 2 of each to form the 'X' cross of "MAS"
        if count_m == 2 and count_s == 2:
            # However, 'M' and 'S' could form 'MAM' or 'SAS' crosses
            # Check that two opposite corners have different chars
            corner_char1 = grid[pos_a[0] - 1][pos_a[1] - 1]
            corner_char2 = grid[pos_a[0] + 1][pos_a[1] + 1]
            if corner_char1 != corner_char2:
                cross_positions.append(pos_a)
    tend = time.time()
    tmap = tend - tstart
    tstart = time.time()

    # NOTE: Other method, single nested loop to construct strings of diagonals
    correct_positions = []
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if grid[r][c] == "A":
                diag1 = grid[r - 1][c - 1] + grid[r + 1][c + 1]
                diag2 = grid[r - 1][c + 1] + grid[r + 1][c - 1]
                if diag1 in ("SM", "MS") and diag2 in ("SM", "MS"):
                    correct_positions.append((r, c))
    tend = time.time()
    tsearch = tend - tstart

    if debug:
        cprint("Time differences of approaches", style="blue")
        cprint(f"Map approach: {tmap*1000:.3f} milliseconds", style="magenta")
        cprint(f"Search approach: {tsearch*1000:.3f} milliseconds", style="yellow")

    return len(cross_positions)


def run() -> None:
    import pathlib

    _DIR = pathlib.Path(__file__).parent
    _EX = str(_DIR / "example.txt")
    _IN = str(_DIR / "input.txt")
    cprint(f"Day {DAY} - {TITLE}", style="bold red")
    cprint()
    cprint("Part 1:")
    cprint()
    msg = "Solution with Example Data:"
    cprint(f"{msg} {part1(_EX, debug=True)}", style="bold green")
    cprint()
    msg = "Solution with Real Data:"
    cprint(f"{msg} {part1(_IN)}", style="bold green")
    cprint()
    cprint("Part 2:")
    cprint()
    msg = "Solution with Example Data:"
    cprint(f"{msg} {part2(_EX)}", style="bold green")
    cprint()
    msg = "Solution with Real Data:"
    cprint(f"{msg} {part2(_IN)}", style="bold green")
    cprint()


if __name__ == "__main__":
    run()


# FIXME: Old failed approach
# def search_by_char(char: str, grid: np.ndarray) -> np.ndarray:
#     found_coords = []
#     for i in range(grid.shape[0]):
#         for j in range(grid.shape[1]):
#             if grid[i, j] == char:
#                 found_coords.append(np.array([i, j], dtype=int))
#     return np.array(found_coords)
#
#
# def cprint_coords(coords: np.ndarray, style: str = "blue") -> None:
#     panels = [Panel(f"[{style}]{(x, y)}[/{style}]") for x, y in coords]
#     cprint(Columns(panels))
#
#
# def cprint_grid(
#     grid: np.ndarray,
#     red_coords: np.ndarray = np.array([]),
#     yel_coords: np.ndarray = np.array([]),
#     grn_coords: np.ndarray = np.array([]),
#     blu_coords: np.ndarray = np.array([]),
# ) -> None:
#     # Init loop vars
#     lines = []
#     red_coords_set = set()
#     if red_coords.size > 0:
#         red_coords_set = set((row, col) for row, col in red_coords)
#     yel_coords_set = set()
#     if yel_coords.size > 0:
#         yel_coords_set = set((row, col) for row, col in yel_coords)
#     grn_coords_set = set()
#     if grn_coords.size > 0:
#         grn_coords_set = set((row, col) for row, col in grn_coords)
#     blu_coords_set = set()
#     if blu_coords.size > 0:
#         blu_coords_set = set((row, col) for row, col in blu_coords)
#
#     for r, row in enumerate(grid):
#         line = ""
#         for c, cell in enumerate(row):
#             if (r, c) in red_coords_set:
#                 line += f"[red]{cell}[/red]"
#             elif (r, c) in yel_coords_set:
#                 line += f"[yellow]{cell}[/yellow]"
#             elif (r, c) in grn_coords_set:
#                 line += f"[green]{cell}[/green]"
#             elif (r, c) in blu_coords_set:
#                 line += f"[blue]{cell}[/blue]"
#             else:
#                 line += cell
#         lines.append(line)
#     for line in lines:
#         cprint(line)
#
#
# def spread_search(
#     char: str, grid: np.ndarray, origins: np.ndarray
# ) -> Tuple[np.ndarray, np.ndarray]:
#     """We'll take a char to search for in a grid of chars by
#     spreading out from the origin coords then checking chars in the grid.
#     """
#     found_coords = []
#     nonadjacent = []
#     # Define spread directions by going clockwise from N from origin
#     spread_vectors = [
#         (-1, -1),  # NW
#         (-1, 0),  # N
#         (-1, 1),  # NE
#         (0, 1),  # E
#         (1, 1),  # SE
#         (1, 0),  # S
#         (1, -1),  # SW
#         (0, -1),  # W
#     ]
#     for origin in origins:
#         adjacent_count = 0
#         for vector in spread_vectors:
#             spread_coord = (origin[0] + vector[0], origin[1] + vector[1])
#             if spread_coord[0] >= grid.shape[0] or spread_coord[1] >= grid.shape[1]:
#                 continue
#             elif spread_coord[0] < 0 or spread_coord[1] < 0:
#                 continue
#             elif grid[spread_coord[0], spread_coord[1]] == char:
#                 found_coords.append(spread_coord)
#                 adjacent_count += 1
#         if adjacent_count == 0:
#             nonadjacent.append(origin)
#     return np.array(found_coords), np.array(nonadjacent)
#
#
# # def filter_nonadjacent(origins: np.ndarray, spreads: np.ndarray) -> np.ndarray:
# #     """From an array of origin coordinates,
# #     Remove any origin coordinates that are not adjacent to any spread coordinates.
# #     """
#
#
# def old_debug_steps1(lines: List[str]) -> int:
#     lines = read_lines(fpath)
#     # Create a numpy matrix of chars from list of strings
#     grid = np.array([list(line) for line in lines])
#     if debug:
#         cprint("\n[blue]grid[/blue]:")
#         cprint(grid)
#
#     # Search for the first letter 'X' in the grid
#     xs = search_by_char("X", grid)
#     if xs.shape[1] != 2:  # Problem if not an array of 2-tuples
#         raise ValueError(f"Expected an array of 2-tuples, not {xs}")
#     if debug:
#         cprint("\n[blue]xs[/blue]:")
#         cprint_coords(xs)
#         print()
#         cprint("\n[blue]hilighted grid[/blue]:")
#         cprint_grid(grid, red_coords=xs)
#
#     # Now search for adjacent 'M's from the found 'X's
#     ms, xna = spread_search("M", grid, xs)
#     if debug:
#         cprint("\n[blue]xs[/blue]:")
#         cprint_coords(xs, style="red")
#         cprint("\n[blue]xna[/blue]:")
#         cprint_coords(xna, style="yellow")
#         cprint("\n[blue]ms[/blue]:")
#         cprint_coords(ms, style="yellow")
#         print()
#         cprint("\n[blue]hilighted grid[/blue]:")
#         cprint_grid(grid, red_coords=xs, yel_coords=ms)
#
#     # Now take the found 'M's and search for adjacent 'A's
#     _as, mna = spread_search("A", grid, ms)
#     if debug:
#         cprint("\n[blue]ms[/blue]:")
#         cprint_coords(ms, style="yellow")
#         cprint("\n[blue]mna[/blue]:")
#         cprint_coords(mna, style="yellow")
#         cprint("\n[blue]as[/blue]:")
#         cprint_coords(_as, style="green")
#         print()
#         cprint("\n[blue]hilighted grid[/blue]:")
#         cprint_grid(grid, red_coords=xs, yel_coords=ms, grn_coords=_as)
#
#     # Now take the found 'A's and search for adjacent 'S's
#     ss, ana = spread_search("S", grid, _as)
#     if debug:
#         cprint("\n[blue]as[/blue]:")
#         cprint_coords(_as, style="green")
#         cprint("\n[blue]ana[/blue]:")
#         cprint_coords(ana, style="green")
#         cprint("\n[blue]ss[/blue]:")
#         cprint_coords(ss, style="blue")
#         print()
#         cprint("\n[blue]hilighted grid[/blue]:")
#         cprint_grid(grid, red_coords=xs, yel_coords=ms, grn_coords=_as, blu_coords=ss)
#     return -1
