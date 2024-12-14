import math
import matplotlib.pyplot as plt
import argparse
import os
from solve import Grid

# Configuration
filename = "./input.txt"
height, width = 103, 101  # Grid dimensions
os.makedirs("./output", exist_ok=True)

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "--mode",
    choices={"exploratory", "threshold", "noninteractive"},
    default="noninteractive",
    help="exploratory: plot the ratio.\n"
    "threshold: interactive threshold analysis.\n"
    "noninteractive: run with predefined threshold (10^8).",
)
args = parser.parse_args()


def compute_steps(grid: Grid, seconds: int):
    """
    Move robots and compute quadrant counts and positions after a given number of seconds.
    """
    grid.move_robots(seconds)
    quadrants = [0, 0, 0, 0]
    xs, ys = [], []

    for robot in grid.robots:
        x, y = robot.pos.x, robot.pos.y
        xs.append(x)
        ys.append(height - y)  # Flip y-axis for plotting

        if x < width // 2 and y < height // 2:
            quadrants[0] += 1
        elif x >= width // 2 and y < height // 2:
            quadrants[1] += 1
        elif x < width // 2 and y >= height // 2:
            quadrants[2] += 1
        elif x >= width // 2 and y >= height // 2:
            quadrants[3] += 1

    return quadrants, xs, ys


def run_threshold_analysis(grid: Grid):
    """
    Interactive mode to find the optimal threshold for ratio filtering.
    """
    threshold = float(input("Insert threshold: "))
    for seconds in range(100000):
        temp_grid = Grid(filename, width, height)  # Reload grid for each iteration
        quadrants, xs, ys = compute_steps(temp_grid, seconds)
        ratio = math.prod(quadrants)

        if ratio < threshold:
            print("Seconds:", seconds)
            plt.figure()
            plt.scatter(xs, ys)
            plt.title(f"Seconds {seconds}")
            plt.savefig(f"./output/Seconds_{seconds}.jpg")
            plt.show()
            keep_going = str(input("Continue (Y/N)? "))
            if keep_going.capitalize() == "N":
                break


def run_noninteractive_analysis(grid: Grid, threshold: int = 10**8):
    """
    Noninteractive mode using a pre-defined threshold to find the first breach, save and display the result.
    """
    for seconds in range(100000):
        temp_grid = Grid(filename, width, height)  # Reload grid for each iteration
        quadrants, xs, ys = compute_steps(temp_grid, seconds)
        ratio = math.prod(quadrants)

        if ratio < threshold:
            print(f"First Threshold Breach at Seconds: {seconds} (Ratio: {ratio})")
            plt.figure()
            plt.scatter(xs, ys)
            plt.title(f"Seconds {seconds}")
            plt.savefig(f"./output/Seconds_{seconds}.jpg")
            plt.show()  # Display the plot
            break  # Exit the loop after finding the first breach


def run_exploratory_analysis(grid: Grid):
    """
    Exploratory mode: Plot the ratio over a range of seconds.
    """
    ratios = []
    for seconds in range(100000):
        temp_grid = Grid(filename, width, height)  # Reload grid for each iteration
        quadrants, _, _ = compute_steps(temp_grid, seconds)
        ratio = math.prod(quadrants)
        ratios.append(ratio)

    plt.figure()
    plt.plot(range(len(ratios)), ratios)
    plt.title("Ratio (output exploratory mode)")
    plt.savefig("./output/ratio_values.jpg")
    plt.show()


# Main execution
grid = Grid(filename, width, height)

if args.mode == "threshold":
    run_threshold_analysis(grid)
elif args.mode == "exploratory":
    run_exploratory_analysis(grid)
else:  # Default to noninteractive mode
    run_noninteractive_analysis(grid)
