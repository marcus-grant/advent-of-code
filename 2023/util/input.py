from typing import List

def input_lines(input_file_path: str) -> List[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines
