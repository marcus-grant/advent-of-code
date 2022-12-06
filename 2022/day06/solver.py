from typing import List
from rich import print

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 10
        self.test2 = 29
        self.part1 = None
        self.part2 = None
    
    def parse(self, instr: str) -> List:
        self.data = [list(line) for line in instr.splitlines()][0]
    
    def solve(self):
        self.part1 = self.find_first_num_unique_chars(4) + 1
        self.part2 = self.find_first_num_unique_chars(14) + 1
        
    def find_first_num_unique_chars(self, num):
        str_buf = []
        i = 0
        for i in range(len(self.data)):
            c = self.data[i]
            if len(str_buf) >= num:
                str_buf.pop(0)
            str_buf.append(c)
            st = set(str_buf)
            if len(st) == num:
                # print(f"Found the [green]packet marker{str_buf} at index {i}[/green] ")
                break
            # print()
            # print(f"Current string set:\t{st}")
            # print(f"Current string buffer:\t{str_buf}")
        return i