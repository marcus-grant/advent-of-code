import numpy as np
from typing import List

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 21
        self.test2 = 8
        self.part1 = 0
        self.part2 = 0
    
    def parse(self, instr: str) -> List:
        lines = instr.splitlines()
        self.data = np.empty(shape=(len(lines), len(lines[0])), dtype=int)
        ri = 0
        ci = 0
        for line in lines:
            ci = 0
            for c in line:
                self.data[ri][ci] = int(line[ci])
                ci += 1
            ri += 1
        del lines

    def trees_behind(self, row: int, col: int) -> np.ndarray[int]:
        res = self.data[:row, col]
        return res
    
    def trees_front(self, row: int, col: int) -> np.ndarray[int]:
        res = self.data[row+1:self.data.shape[0], col]
        return res
    
    def trees_left(self, row: int, col: int) -> np.ndarray[int]:
        res = self.data[row, :col]
        return res
    
    def trees_right(self, row: int, col: int) -> np.ndarray[int]:
        res = self.data[row, col+1:self.data.shape[1]]
        return res
    
    def tree_is_visible(self, row: int, col: int) -> bool:
        # set the max height (ie one less than the tree being checked)
        max_height = self.data[row][col] - 1
        # get all the trees in each axis, one tree array for each axis of the outer list 
        trees_axis_fns = [
            self.trees_behind,
            self.trees_front,
            self.trees_left,
            self.trees_right,
        ]
        # Loop through each list of tree arrays of an axis
        for tree_axis_fn in trees_axis_fns:
            trees_in_axis = tree_axis_fn(row, col)
            # Assume the tree is visible in this axis
            visible_in_axis = True
            # Loop through every tree in the axis
            for tree in trees_in_axis:
                # If any tree is larger than the max height in this axis
                if tree > max_height:
                    # Then it's not visible in this axis, leave loop
                    visible_in_axis = False
                    break
            # If the tree is visible in any axis - then it's visible somewhere
            if visible_in_axis:
                return True
        # If the tree is visible in no axis, it's not visible somewhere
        return False

    def solve(self):
        ### Part 1 ###

        visible_inner_trees = 0
        trees_shape = self.data.shape
        # Loop through every tree cell row/col index of INNER trees
        for ri in range(1, trees_shape[0] - 1):
            row = self.data[ri]
            for ci in range(1, trees_shape[1] - 1):
                if self.tree_is_visible(ri, ci):
                    visible_inner_trees += 1
        
        edge_trees_count = 2 * ((trees_shape[0] - 1) + (trees_shape[1] - 1))
        self.part1 = visible_inner_trees + edge_trees_count

        ### Part 2 ###
