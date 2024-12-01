from colorama import Fore, Back, Style
from pprint import pprint
from pydantic import BaseModel
from typing import Tuple

def print_solution(sol: str, title: str=''):
    s = f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.CYAN}Solution"
    if len(title) > 0:
        s += f" to {title}"
    s += f"{Style.RESET_ALL}: {Back.LIGHTCYAN_EX}{Fore.BLACK}{sol}{Style.RESET_ALL}"
    print(s)

def pprint_grid(grid: list[list[str]]) -> None:
    for row in grid:
        for element in row:
            if element.isdigit():
                print(f"{Fore.GREEN}{element}{Style.RESET_ALL}", end="")
            elif element != ".":
                print(f"{Fore.RED}{element}{Style.RESET_ALL}", end="")
            else:
                print(element, end="")
        print()

def read_input(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

class Part(BaseModel):
    symbol: str
    row: int
    col: int

    def __repr__(self):
        return f"({self.symbol}, {self.col}, {self.row})"
    
class PartNumber(BaseModel):
    value: str
    row: int
    col: int # The left-most or first digit of the number is the col position
    length: int
    adjacent_parts: list[Part] = []

    def __init__(self, value: str, row: int, col: int):
        length = len(value) 
        super().__init__(value=value, row=row, col=col, length=length)
    
    def __repr__(self):
        return f"({self.value}, {self.col}, {self.row})"
    
    def part_is_adjacent(self, part: Part) -> bool:
        # First determine if the part is on same row
        if part.row == self.row:
            if part.col == self.col - 1: # If so, check left of col
                return True
            # Check if the last digit of partnum is adjacent to part
            elif part.col == self.col + self.length:
                return True
            else: # Exit early, if on same row but not adjacent
                return False
        # If not, it might be vertically adjacent which
        # is when a col is the same or within length of col to the right.
        # Notably diagonals just extend the range by one on each side.
        if self.col - 1 <= part.col <= self.col + self.length:
            # If adjacent vertically or diagonally, row should be +/- 1
            if abs(part.row - self.row) == 1:
                return True
            else:
                return False
        return False # If you're here, it's not adjacent

class Grid(BaseModel):
    width: int
    height: int
    cells: list[list[str]]

    def __init__(self, input_file):
        cells = [list(row) for row in read_input(input_file)]
        height = len(cells)
        width = len(cells[0])
        super().__init__(width=width, height=height, cells=cells)
    
    # def pprint(self) -> None:
    #     for row in self.cells:
    #         for element in row:
    #             if element.isdigit():
    #                 print(f"{Fore.GREEN}{element}{Style.RESET_ALL}", end="")
    #             elif element != ".":
    #                 print(f"{Fore.RED}{element}{Style.RESET_ALL}", end="")
    #             else:
    #                 print(element, end="")
    #         print()

    def pprint(self, adjacents: list[Part] = []) -> None:
        s = ''
        for r in range(self.height):
            row = self.cells[r]
            for c in range(self.width):
                cell = row[c]
                if cell == '.':
                    s += '.'
                    continue
                if cell.isdigit():
                    s += f"{Fore.GREEN}{cell}{Style.RESET_ALL}"
                    continue
                for p in adjacents:
                    if p.row == r and p.col == c:
                        s += f"{Fore.RED}{cell}{Style.RESET_ALL}"
                        continue
                s += f"{Fore.BLUE}{cell}{Style.RESET_ALL}"
            print(s)
            s = ''
    
    def find_parts(self) -> list[Part]:
        parts = []
        for y in range(self.height):
            row = self.cells[y]
            for x in range(self.width):
                cell = row[x]
                if (not '.' in cell) and (not cell.isdigit()):
                    parts.append(Part(symbol=cell, col=x, row=y))
        return parts
    
    def find_part_numbers(self) -> list[PartNumber]:
        part_numbers: list[PartNumber]=[]
        for y in range(self.height):
            row = self.cells[y]
            buf_string = ''
            buf_start = 0
            for x in range(self.width):
                cell = row[x]
                if cell.isdigit(): # If cell is digit, append to buffer
                    if len(buf_string) == 0:
                        buf_start = x
                    buf_string += cell
                    continue
                if len(buf_string) > 0:
                    part_num = PartNumber(
                        value=buf_string,
                        col=buf_start,
                        row=y)
                    part_numbers.append(part_num)
                    buf_string = ''
                    buf_start = 0
        return part_numbers
    
    
def part1(input_file: str) -> int:
    """ Solve part 1 with an 'input' file path, return solution """
    # grid = [list(row) for row in read_input(input)]
    grid = Grid(input_file)
    grid.pprint()
    parts = grid.find_parts()
    print(f"Parts in Grid above: {parts}")
    part_nums = grid.find_part_numbers()
    print(f"Part#s in Grid above: {part_nums}")
    # Go through every part & number and determine if they are adjacent
    for p in parts:
        for n in part_nums:
            if n.part_is_adjacent(p):
                n.adjacent_parts.append(p)
    nums_with_parts = [n for n in part_nums if len(n.adjacent_parts) > 0]
    parts_with_nums = [n.adjacent_parts for n in nums_with_parts]
    parts_with_nums = [p[0] for p in parts_with_nums]
    grid.pprint(adjacents=parts_with_nums)
    print(f"Part#s with adjacent parts: {[n.value for n in nums_with_parts]}")
    solution = sum([int(n.value) for n in nums_with_parts])
    return solution

def main():
    print()
    print("Part 1 - Example")
    print("================")

    solution = part1('03/example.txt')
    print_solution(f"\n{solution}\n", title="Part 1 Example")

    print("Part 1 - Real Input")
    print("===================")

    # solution = part1('03/input.txt')
    # print

    print("Part 2 - Example")
    print("================")
    
    # TODO

    print("Part 2 - Test")
    print("================")

    # TODO


if __name__ == "__main__":
    print("=============== Day 03 - Gear Ratios ===============")
    main()
    print("================ Day 03 - Complete =================")