# def read_input(input_file="./01/input.txt"):
#     with open(input_file, "r") as file_buf:
#         input_lines = file_buf.read().splitlines()
#     return input_lines
from ..util.input import input_lines

def find_digit(line: str, reverse: bool = False) -> str:
    digit_dict = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }

    start = 0
    end = len(line) + 1
    step = 1

    if reverse:
        start = -1
        end *= -1 
        step *= -1
    
    # Char by char, search for numbers,
    # avoiding situations where numbers overlap like 'eightwo' = 82

    for i in range(start, end, step):
        if line[i].isdigit():
            return line[i]
        if reverse:
            substr = line[i:]
        else:
            substr = line[:i + step]
        
        for word, digit in digit_dict.items():
            if word in substr:
                return digit


def solver_part1(input_lines: list[str]) -> int:
    numeric_only_lines = []
    for line in input_lines:
        new_line = ''.join([i for i in line if i.isdigit()])
        numeric_only_lines.append(new_line)

    first_last_digits = [f'{line[0]}{line[-1]}' for line in numeric_only_lines]
    numbers = [int(s) for s in first_last_digits]
    solution = sum(numbers)
    return solution

def digits_in_string(s: str) -> list[int]:
    words = [
        'zero', 'one', 'two', 'three', 'four',
        'five', 'six', 'seven', 'eight', 'nine',
    ]
    digits = []
    str_buf = ""
    for char in s:
        if char.isnumeric():
            digits.append(int(char))
            str_buf = ""
        str_buf += char
        for i, word in enumerate(words):
            if word.startswith(str_buf):
                if word == str_buf:
                    digits.append(i)
                    str_buf = ""
                break

    return digits

def solver2(input_lines: list[str]) -> int:
    digits = []

    # find the first and last occurrence on each line of a digit
    for line in input_lines:
        first_digit = find_digit(line)
        last_digit = find_digit(line, reverse=True)
        digits.append(f"{first_digit}{last_digit}")
    
    digits = [int(s) for s in digits]
    solution = sum(digits)
    return solution

def check_example(actual: int, expected: int) -> bool:
    if actual == expected:
        print(f"Example solution of {actual} correct!")
        return True
    else:
        print("Example failed:")
        print(f"Expected: {expected}, Actual: {actual}")
        return False

def main():
    # Set expected solution to example
    solution_example_expected = 142
    # Read example file
    example_lines = read_input(input_file="./01/example.txt")
    print(example_lines) 
    solution_example_actual = solver_part1(example_lines)
    result_example = check_example(
        solution_example_actual,
        solution_example_expected
    )
    if not result_example:
        raise Exception("Example failed")
    else:
        print("Example solution works!")
    
    # Input solution
    input_lines = read_input()
    solution_part1 = solver_part1(input_lines)
    print("Solution to part1: ", solution_part1)

    # Part 2
    solution_example2_expected = 281
    example_lines = read_input(input_file="./01/example2.txt")
    solution_example_actual = solver2(example_lines)
    result_example = check_example(solution_example_actual, solution_example2_expected)
    if not result_example:
        raise Exception("Example failed, exiting!")
    solution_part2 = solver2(input_lines)
    print("Solution to part2: ", solution_part2)

if __name__ == "__main__":
    main()