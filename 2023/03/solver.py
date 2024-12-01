# from typing import List, Tuple
# # from lib.parse import parse_string_grid

# ### LIB PARSE ###
# import re

# def parse_group_of_integers(file: str) -> List[List[int]]:
#     """
#     Parses a list of integers that is split by spaces
#     Example:
#     123
#     456
#     789
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     output = []

#     curr = []
#     for l in lines:
#         l = l.strip()
#         if l == "":
#             output.append(curr)
#             curr = []
#         else:
#             curr.append(int(l))
#     if len(curr) > 0:
#         output.append(curr)

#     return output

# def parse_string_pairs(file: str) -> List[List[str]]:
#     """
#     Parses a pair of two string values split by a space
#     Example:
#     A B
#     C D
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     output = []

#     for l in lines:
#         output.append(l.strip().split(' '))
#     return output

# def parse_integer_pairs(file: str) -> List[Tuple[int, int]]:
#     """
#     Parses a pair of two integer values split by a comma & space
#     Example:
#     1, 2
#     3, 4
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     output = []

#     for l in lines:
#         pair = l.strip().split(', ')
#         output.append([int(pair[0]), int(pair[1])])
#     return output

# def parse_strings(file: str) -> List[str]:
#     """
#     Parses a list of strings
#     Example:
#     ABC
#     DEF
#     """
#     input = open(file, 'r')
#     return [x.strip() for x in input.readlines()]

# def parse_range_of_integer_pairs(file: str) -> List[List[Tuple[int]]]:
#     """
#     Parses ranges of integers split by a comma
#     Example:
#     1-2,3-4
#     5-6,7-8
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     output = []

#     for l in lines:
#         local = []
#         ranges = l.strip().split(',')
#         for pair in ranges:
#             v1, v2 = pair.split('-')
#             local.append([int(v1), int(v2)])
#         output.append(local)
    
#     return output

# def parse_string_lists(file: str) -> List[List[str]]:
#     """
#     Parses a list of strings for each line with undefined length
#     Example:
#     A B C
#     D E
#     F G H
#     """
#     input = open(file, 'r')
#     return [x.strip().split(' ') for x in input.readlines()]

# def parse_integer_grid(file: str) -> List[List[int]]:
#     """
#     Parses a 2D matrix of integers
#     Example:
#     123
#     456
#     789
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     grid = []

#     for row in lines:
#         parsed_row = [int(x) for x in row.strip()]
#         grid.append(parsed_row)
    
#     return grid

# def parse_string_grid(file: str) -> List[List[str]]:
#     """
#     Parses a 2D matrix of string characters
#     Example:
#     ABC
#     DEF
#     GHI
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     grid = []
#     longest_row = 0

#     for row in lines:
#         parsed_row = [x for x in row.rstrip()]
#         grid.append(parsed_row)
#         longest_row = max(longest_row, len(row))
    
#     for r in range(len(grid)):
#         to_add = longest_row - len(grid[r])
#         for _ in range(to_add):
#             grid[r].append(" ")

#     return grid

# def parse_string_integer_tuples(file: str) -> List[Tuple[str, int]]:
#     """
#     Parses a tuple consisting of a string and integer value
#     Example:
#     A 1
#     B 2
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     output = []

#     for l in lines:
#         l = l.strip().split(' ')
#         output.append([l[0], int(l[1])])
    
#     return output

# def parse_integers(file: str) -> List[int]:
#     """
#     Parses a list of integers
#     Example:
#     +1
#     -2
#     +3
#     """
#     input = open(file, 'r')
#     return [int(x.strip()) for x in input.readlines()]

# def parse_x_y_pairs(file: str) -> List[Tuple[str, str]]:
#     """
#     Parses a list of x/y pairs and gets their values as strings
#     Example:
#     x=495, y=2..7
#     y=7, x=495..501
#     """
#     input = open(file, 'r')
#     lines = input.readlines()
#     output = []

#     for l in lines:
#         l = l.strip().split(", ")
#         if l[0][0:2] == "x=":
#             output.append([l[1][2:], l[0][2:]])
#         else:
#             output.append([l[0][2:], l[1][2:]])
    
#     return output
# ### END LIB PARSE ###

# NON_SYMBOLS = {"0","1","2","3","4","5","6","7","8","9","."," "}

# def is_adj(grid: List[List[any]], coords: List[Tuple[int, int]]) -> bool:
#     adj = [[-1,-1], [-1,0], [-1,1], [0,-1], [0, 1], [1,-1], [1,0], [1,1]]
    
#     for pair in coords:
#         for r_offset, c_offset in adj:
#             row, col = pair[0] + r_offset, pair[1] + c_offset
#             if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]) or grid[row][col] in NON_SYMBOLS:
#                 continue
#             else:
#                 return True
#     return False

# def get_numbers(grid: List[List[any]]) -> List[Tuple[int, Tuple[int, int]]]:
#     numbers = []
#     for r in range(len(grid)):
#         num, coords = "", []
#         for c in range(len(grid[0])):
#             if grid[r][c] in NON_SYMBOLS and grid[r][c] != "." and grid[r][c] != " ":
#                 num += grid[r][c]
#                 coords.append([r,c])
#             elif len(num) > 0:
#                 numbers.append([int(num), coords])
#                 num, coords = "", []

#         if len(num) > 0:
#             numbers.append([int(num), coords])
#             num, coords = "", []
    
#     return numbers

# def get_part_numbers() -> int:
#     grid = parse_string_grid("03/input.txt")
#     numbers = get_numbers(grid)
#     res = 0

#     for val, coords in numbers:
#         if is_adj(grid, coords):
#             res += val
#     return res

# print(get_part_numbers())

# def has_symbol(grid, r, c):
#     for dx in (-1, 0, 1):
#         for dy in (-1, 0, 1):
#             if dx == 0 and dy == 0:
#                 continue
#             if (r + dy) < 0 or (r+dy) >= len(grid) or (c + dx) < 0 or (c + dx) >= len(grid[0]):
#                 continue
#             # print("look at", r+dy, c+dx, "from", r, c, grid[r+dy][c+dx])
#             if not grid[r+dy][c+dx].isdigit() and grid[r+dy][c+dx] != '.':
#                 return True
#     return False


# def solve(puzzle_input):
#     rows = puzzle_input.split("\n")

#     total = 0

#     for r, row in enumerate(rows):
#         c = 0
#         n = ""
#         symbol = False
#         while c < len(row):
#             if row[c].isdigit():
#                 n += row[c]
#                 # print("found", n, "in", r, c)
#                 if not symbol and has_symbol(rows, r, c):
#                     symbol = True
#             else:
#                 # print("not", row[c], "symbol", symbol, "so far", n)
#                 if symbol and len(n) > 0:
#                     total += int(n)
#                 symbol = False
#                 n = ""
#             c += 1
#         if symbol and len(n) > 0:
#             total += int(n)


#     return total

# if __name__ == "__main__":
#     # Read file into one long string
#     with open("03/example.txt", "r") as f:
#         TEST_INPUT = f.read()
#     with open("03/input.txt", "r") as f:
#         PUZZLE_INPUT = f.read()
#     assert solve(TEST_INPUT) == 4361, solve(TEST_INPUT)
    # print(solve(PUZZLE_INPUT))

# import csv

# """
# List of indexes where signs and numbers occur
# """
# signs_index_list = []
# numbers_index_list = []
# cog_index_list = []
# """
# Helps creating a matrix format line_indicator x index in list
# """
# line_indicator = 1
# """
# Number and signs (not including .  <-- dot)
# """
# numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# signs = ['!', '@', '#', "$", '%', '^', '&', '*', '(', ')', '-', '+', '=', '/']
# res = 0
# cog = '*'

# with open("03/input.txt") as file:
#     file = csv.reader(file)
#     for line in file:
#         """
#         Opening the file and splitting each line to become list of each char
#         """
#         split = [*(line[0])]
#         """
#         Index list of number occurrence
#         """
#         index_list = []
#         """
#         Will help create full number and turn it to the int
#         """
#         number = ''
#         """
#         First for loop checks if char is in signs list if yes it add it to our list all
#         occurrences of special signs. Format: [1st argument nr of line, 2nd argument index in this line]
#         """
#         for index, letter in enumerate(split):
#             if letter in signs:
#                 signs_index_list.append([line_indicator, index])
#         """
#         Second for loop checks if char is in numbers.
#         """

#         for index, letter in enumerate(split):
#             """
#             First part just check for individual char because it is string. Then concat it to var number.
#             Second part append to the index_list  occurrence of number.
#             Format: [1st argument nr of line, 2nd argument index in this line]. 
#             """
#             if letter in numbers:
#                 number += letter
#                 index_list.append([line_indicator, index])
#             """
#             This if checks if var number is not an empty string (it would mean previous char/chars were in numbers)
#             and are stored in var number. If next char is not number or it is end of the line, join the char in str
#             (so far they were just separated chars in list). Next Step we reset number var for next number.
#             Finally append it in format [1st argument: int full number, 
#             2nd argument: list withing list of all occurrences of number 
#             [1st argument nr of line, 2nd argument index in this line]].
#             """
#             if (letter not in numbers and number != '') or (number != '' and index == len(split) - 1):
#                 number_to_calc = ''.join(number)
#                 number = ''
#                 numbers_index_list.append([int(number_to_calc), index_list])
#                 index_list = []

#         """
#         Here where we add to line indicator when we read entire line.
#         """
#         line_indicator += 1
#         """
#         Last loop where we compare if each full number is attached to any sign.
#         In element[1] we have list of lists example : [[],[],[]] and each list inside has to be compared
#         with sings_index_lists. If they match we add number element[0] to res and break the loop.
#         (The reason we use break is simple fact that each number might be attached to more than on sign.
#         We want to check if it is attached to any so one time we add it to result.
#         """
#     for element in numbers_index_list:
#         for indexes in element[1]:
#             """Check right, left , down,  down-left, down-right, up, up-left, up-right"""
#             if [int(indexes[0]), int(indexes[1] + 1)] in signs_index_list or \
#                 [int(indexes[0]), int(indexes[1] - 1)] in signs_index_list or \
#                 [int(indexes[0]) - 1, int(indexes[1])] in signs_index_list or \
#                 [int(indexes[0]) - 1, int(indexes[1] - 1)] in signs_index_list or \
#                 [int(indexes[0]) - 1, int(indexes[1] + 1)] in signs_index_list or \
#                 [int(indexes[0]) + 1, int(indexes[1])] in signs_index_list or \
#                 [int(indexes[0]) + 1, int(indexes[1] - 1)] in signs_index_list or \
#                 [int(indexes[0]) + 1, int(indexes[1]) + 1] in signs_index_list:
#                 res += element[0]
#                 break

# print(res)

# """Second star.  hold_first_number - holds first number to multiply"""

# res2 = 0
# hold_first_number= 0


# """Same approach as in part 1 only now we check list of cogs in list of indexes of numbers"""
# for cog in cog_index_list:
#     """Set hold_first_number to zero when we checking next cog. Three possible outcomes.
#     1. Cog is not attached to any number. hold_first_number was 0 in that case 
#     2. Cog is attached to one number. We are moving to next cog. hold_first_number has to be set back to 0
#     3. Cog is attached to two numbers. If statement hold_first_number > 0. 
#     """
#     hold_first_number = 0
#     for index in numbers_index_list:
#         """Check right, left , down,  down-left, down-right, up, up-left, up-right"""
#         if [int(cog[0]), int(cog[1] + 1)] in index[1] or \
#                 [int(cog[0]), int(cog[1] - 1)] in index[1] or \
#                 [int(cog[0]) - 1, int(cog[1])] in index[1] or \
#                 [int(cog[0]) - 1, int(cog[1] - 1)] in index[1] or \
#                 [int(cog[0]) - 1, int(cog[1] + 1)] in index[1] or \
#                 [int(cog[0]) + 1, int(cog[1])] in index[1] or \
#                 [int(cog[0]) + 1, int(cog[1] - 1)] in index[1] or \
#                 [int(cog[0]) + 1, int(cog[1]) + 1] in index[1]:
#             print(index[0])
#             if hold_first_number > 0:
#                 """
#                 Cog is attached to number we multiply first number which we stored in hold_first_number by index[0]
#                 which is second number attached to cog.
#                 hold_first_number set to 0 because there might be more cogs on the same line of text.
#                 """
#                 res2 += hold_first_number * index[0]
#                 hold_first_number = 0
#             """
#             Add current number attached to cog to var.
#             """
#             hold_first_number += index[0]


# print(res2)

# from typing import List, Tuple

# SchematicList = List[List[str]]
# Pos = Tuple[int, int]

# schematic_2d: SchematicList = []

# with open('03/input.txt') as f:
#     for y, line in enumerate(f.readlines()):
#         # print(len(line))
#         schematic_2d.append([])
#         for x, character in enumerate(line.strip()):
#             schematic_2d[y].append(character)

# def clamp(number):
#     return max(0, min(number, 139))


# class Digiloc:
#     locating_digit: bool
#     digits: List
#     start_pos: Pos
#     found: bool

#     def __init__(self) -> None:
#         self.digits = []
#         self.start_pos = (0,0)
#         self.end_pos = (0,0)

#         self.locating_digit = False

#     def input(self, char: str, pos: Pos) -> bool:
#         if char.isdigit():
#             if not self.locating_digit:
#                 self.locating_digit = True
#                 self.start_pos = pos
#             self.digits.append(char)
#         else:
#             if self.locating_digit:
#                 # new number found
#                 self.found = True
#                 self.end_pos = pos
#                 return True
#             self.locating_digit = False
#         return False

#     def flush(self) -> Tuple[int, Pos]:
#         if self.found:
#             number = int("".join(self.digits))
#             pos = self.start_pos
#             end_pos = self.end_pos

#             self.start_pos = (0,0)
#             self.end_pos = (0,0)
#             self.digits = []
#             self.found = False
#             self.locating_digit = False
#             return (number, pos, end_pos)


# class Schematic:
#     numbers: List[Tuple[Pos, Pos, int]]
#     schematic_2d: SchematicList
#     symbols: List
#     gears: List[Tuple[Pos, int]]
#     gear_pos: dict
#     def __init__(self, schematic_2d: SchematicList) -> None:
#         self.schematic_2d = schematic_2d
#         self.numbers = []
#         self.symbols = []
#         self.gears = []
#         self.gear_pos = {}

#         self.save_numbers()

#     def print(self):
#         for y in self.schematic_2d:
#             for x in y:
#                 print(x, end='')
#             print('')

#     def save_numbers(self):
#         digiLoc = Digiloc()
#         for y, y_list in enumerate(self.schematic_2d):
#             for x, character in enumerate(y_list):
#                 pos = (x, y)
#                 if digiLoc.input(character, pos):
#                     (number, start_pos, end_pos) = digiLoc.flush()
#                     self.numbers.append((start_pos, end_pos, number))
#                 else:
#                     if not character.isalnum() and character != '.':
#                         self.symbols.append(character)
                
#                 if character == '*':
#                     self.gears.append((pos, character))
#                     self.gear_pos[pos] = []

#         self.symbols = set(self.symbols)

#     def check_adjacency(self, idx):
#         # print(self.symbols)
#         (pos, end_pos, number) = self.numbers[idx]
#         digits = len(str(number))
#         # print(pos, number)
        
#         # (left, top), (right, bottom)
#         box = (
#             (clamp(pos[0] - 1), clamp(pos[1] - 1)),
#             (clamp(pos[0] + digits), clamp(pos[1] + 1))
#         )

#         y = box[0][1]
#         end_x = box[1][0]
#         end_y = box[1][1]
#         has_special_symbol = False
#         has_gear = False
#         while y <= end_y:
            
#             x = box[0][0]
#             while x <= end_x:
#                 character = self.schematic_2d[y][x]
#                 # print(character, end='')

#                 if not has_special_symbol and character in self.symbols:
#                     # print("special!")
#                     has_special_symbol = True

#                 if not has_gear and character == "*":
#                     has_gear = True
#                     self.gear_pos[(x, y)].append(number)

#                 x = x+1
#             # print('')
#             y = y+1
#         # print(box)
#         return {
#             "has_special_symbol": has_special_symbol,
#             "has_gear": has_gear
#         }

#     def print_adjacency(self, idx, type='numbers'):
#         if type  == 'numbers':
#             (pos, number) = self.numbers[idx]
#         elif type == 'gears':
#             (pos, number) = self.gears[idx]
#         else:
#             return
        
#         print(pos, number)

#         digits = len(str(number))

#         # (left, top), (right, bottom)
#         box = (
#             (clamp(pos[0] - 1), clamp(pos[1] - 1)),
#             (clamp(pos[0] + digits), clamp(pos[1] + 1))
#         )

#         y = box[0][1]
#         end_x = box[1][0]
#         end_y = box[1][1]
#         while y <= end_y:
            
#             x = box[0][0]
#             while x <= end_x:
#                 character = self.schematic_2d[y][x]
#                 print(character, end='')
#                 x = x+1
#             print('')
#             y = y+1


# schematic = Schematic(schematic_2d)

# def test_1(schematic: Schematic):
#     s = 0
#     for i, number in enumerate(schematic.numbers):
#         if schematic.check_adjacency(i):
#             print(number)
#             s = sum([s, number[1]])
#     print(s)

# test_1(schematic)

# def test_2(schematic: Schematic):
#     s = 0
#     i = 0
#     # checks = schematic.check_adjacency(i)
#     # print(checks["has_gear"])
#     schematic.print_adjacency(0,'gears')

#     for i, number in enumerate(schematic.numbers):
#         schematic.check_adjacency(i)
            

#     for k, v in schematic.gear_pos.items():
#         if len(v) == 2:
#             print(k, v, end='')
#             val = v[0] * v[1]
#             print('', val)

#             s = sum([s, val])
#     print(s)


    
# test_2(schematic)

maxX, maxY = 9, 9
maxX, maxY = 139, 139

def getSymbols(fileLines):
    res = []
    for i, line in enumerate(file):
        for j, c in enumerate(line):
            if c == '*':
                res.append([i, j, c])
    return res

def getSpots(x,y):
    x = x + 1 if x < 0 else x
    x = x - 1 if x > maxX else x
    y = y + 1 if y < 0 else y
    y = y - 1 if y > maxY else y

    return [x, y]

def eight(x,y):
    res = []
    for i in range(-1,2):
        for j in range(-1,2):
            res.append(getSpots(x + i, y + j))
    return res

def getNumbers(x,y, file):
    res = file[x][y]
    pos = set()
    pos.add((x,y))
    newY = y + 1
    while newY <= maxY and file[x][newY].isdigit():
        res = res + file[x][newY]
        pos.add((x,newY))
        newY = newY + 1
    newY = y - 1
    while newY >= 0 and file[x][newY].isdigit():
        res = file[x][newY] + res
        pos.add((x,newY))
        newY = newY - 1
    return (res, pos)
# input ='inputs/test.txt'
input ='03/input.txt'

with open(input, 'r') as f:
    file = f.read().replace(',','').splitlines()
    
    symbols = getSymbols(file)
    #print(symbols)
    eights = []
    for x in symbols:
        eights.append(eight(x[0],x[1]))
    print('8:', eights)
    total = 0
    for x in eights:
        digits = list(filter(lambda x: file[x[0]][x[1]].isdigit(),x))

        nums = []
        for x in digits:
            res = getNumbers(x[0],x[1],file)
            nums.append(res)
        unique = []
        for x in nums:
            add = True
            for y in unique:
                if add is False:
                    continue
                if x[0] == y[0] and x[1] == y[1]:
                    add = False
                    continue
            if add:
                unique.append(x)
        if len(unique)  == 2:
            total = total + int(unique[0][0]) * int(unique[1][0])
    
    print(total)



            
