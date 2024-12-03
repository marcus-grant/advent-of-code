import numpy as np
from typing import List


def read_lines(fpath: str) -> List[str]:
    with open(fpath, "r") as f:
        lines = f.read().splitlines()
    return lines


def is_safe(report: np.ndarray) -> bool:
    """
    Determine if a report is "safe" based on the following rules:
    - The levels are either **all increasing** or **all decreasing**
    - Any two adjacent levels differ by at least 1 & at most 3
    """
    # First compute the difference array as it will be used in all checks
    diffs = np.diff(report)

    # Create boolean flags for increasing & decreasing levels
    increasing = np.all(diffs > 0)
    decreasing = np.all(diffs < 0)

    # If every level isn't either ALL increasing or...
    # ALL decreasing, the report isn't considered safe
    if not (increasing or decreasing):
        return False

    # This check concerns magnitudes, so make diffs absolute values
    diffs = np.abs(diffs)

    # Check if the differences between adjacent levels are within the range
    if np.any(diffs > 3):
        return False

    if np.any(diffs < 1):
        return False

    # If all checks pass, the report is safe
    return True


def part1(fpath: str, debug: bool = False) -> int:
    """
    Each line is a "report" with whitespace separated numbers.
    Each report is "safe" according to rules in description of is_safe function.
    """
    lines = read_lines(fpath)

    # Each report is a list of integers, so split by whitespace & parse to int
    # Use numpy for faster batch processing
    reports = [np.array(list(map(int, line.split()))) for line in lines]

    safe_reports = 0  # The counter for safe reports
    # Loop through each report and apply rules to determine if it is safe
    for report in reports:
        if is_safe(report):
            # If report is safe, increment the counter
            safe_reports += 1

    return safe_reports


def problem_damper(report: np.ndarray) -> np.ndarray:
    """
    There's a safety system called the "problem damper" that
    will remove exactly one level problem from a reactor.
    This changes whether a report is safe because
    there's a margin of one unsafe level for each report allowed.
    This simulates the problem damper by going through the report 1 lvl @ a time.
    Removing that one level in modified report and
    seeing if it can be safe safe without that level.
    If it can at any point, return the modified report.
    Otherwise after trying all possible modifications, return the original report.
    """
    for i in range(len(report)):
        modified_report = np.delete(report, i)
        if is_safe(modified_report):
            return modified_report
    return report


def part2(fpath: str, debug: bool = False) -> int:
    """
    Each line is a "report" with whitespace separated numbers.
    Each report is "safe" according to rules in description of is_safe function.
    In part2 however, it's determined that a "safety damper" exists.
    It is modeled by the problem_damper function.
    It removes one unsafe level from operation.
    That means a report that is unsafe due only to one level can be made safe.
    """
    lines = read_lines(fpath)

    # Each report is a list of integers, so split by whitespace & parse to int
    # Use numpy for faster batch processing
    reports = [np.array(list(map(int, line.split()))) for line in lines]

    safe_reports = 0  # The counter for safe reports
    for report in reports:
        # Check if report is safe
        if is_safe(report):
            safe_reports += 1
            continue
        # If not, apply the damper to see if it can be made safe
        modified_report = problem_damper(report)
        # If the lengths are different, the damper worked
        if len(modified_report) != len(report):
            safe_reports += 1

    # The answer to part2 is the number of safe reports after applying the damper
    return safe_reports
