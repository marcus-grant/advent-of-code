import pprint

# pprinter = pprint.PrettyPrinter(indent=4)
# pp = pprinter.pprint

from pp import (get_colorized_round, get_colorized_game,
                print_game, print_games, print_solution)

def input_lines(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

def game_marker_index(game_str: str) -> int:
    for i in range(len(game_str)):
        if game_str[i] == ':':
            if game_str[i+1] == ' ':
                return i + 2

def strip_game_marker(game_str: str) -> str:
    game_str = game_str[game_marker_index(game_str):]
    return game_str

def parse_count(cubes_str: str) -> tuple[int, int, int]:
    # Remove possible leading whitespace
    cubes_str = cubes_str.lstrip()
    # Pull out the number from the string as int
    num_str = ''
    for i in range(len(cubes_str)):
        if not cubes_str[i].isdigit():
            break
        num_str += cubes_str[i]
    num = int(num_str)
    if 'red' in cubes_str:
        return (num, 0, 0)
    if 'green' in cubes_str:
        return (0, num, 0)
    if 'blue' in cubes_str:
        return (0, 0, num)

def parse_round(round_str: str) -> tuple[int, int, int]:
    cube_strs = round_str.split(',')
    cubes = [parse_count(cube) for cube in cube_strs]
    round_total = (0, 0, 0)
    round_total = tuple(sum(x) for x in zip(*cubes))
    return round_total

def parse_game(game_str: str) -> list[tuple[int, int, int]]:
    rounds_strs = game_str.split(';')
    rounds = [parse_round(round_str) for round_str in rounds_strs]
    return rounds

def max_of_game(rounds: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    mg = (0, 0, 0)
    # Loop through rounds and update mg or the max of every round
    # at each index of the tuple representing a color
    for rnd in rounds:
        mg = tuple(max(x) for x in zip(mg, rnd))
    return mg

def solver1(input_file: str):
    # Read input data lines & strip game # marker substrings from each game line
    games_strs = [strip_game_marker(g) for g in input_lines(input_file)]
    # Parse each row (game) into a list of tupes (round) of 3 cube color counts
    games_with_rounds = [parse_game(g) for g in games_strs]
    # Get the maximum of each color needed in a game
    game_maxes = [max_of_game(g) for g in games_with_rounds]
    MAX = (12, 13, 14) # R, G, B
    game_ids_possible = [
        i + 1 for i, g in enumerate(game_maxes)
            if MAX[0] >= g[0] and MAX[1] >= g[1] and MAX[2] >= g[2]]
    solution = sum(game_ids_possible)
    return (solution, games_with_rounds, game_maxes, game_ids_possible)

def solver2(input_file: str):
    game_strs = [strip_game_marker(g) for g in input_lines(input_file)]
    games_with_rounds = [parse_game(g) for g in game_strs]
    game_maxes = [max_of_game(g) for g in games_with_rounds]
    game_powers = [gm[0] * gm[1] * gm[2] for gm in game_maxes]
    solution = sum(game_powers)
    return (
        games_with_rounds,
        game_maxes,
        game_powers,
        solution
    )



def main():
    print("Part 1 - Example")
    print("================")
    (solution, games_with_rounds,
     game_maxes, game_ids_possible) = solver1('02/example1')

    print("\nEach Row a Game - Rounds in Format: (R,G,B)")
    print("===========================================")
    print_games(games_with_rounds)

    print("\nGame Maxes (R,G,B): ")
    print_game(game_maxes)

    print(f"Game IDs that are Possible: {game_ids_possible}")
    print()
    print_solution(solution, title='First Example')

    print("Part 1 - Test")
    print("=============")
    (solution, games_with_rounds,
     game_maxes, game_ids_possible) = solver1('02/input')

    print("\nEach Row a Game - Rounds in Format: (R,G,B)")
    print("===========================================")
    print_games(games_with_rounds)

    print("\nGame Maxes (R,G,B): ")
    print_game(game_maxes)

    print(f"Game IDs that are Possible: {game_ids_possible}")
    print()
    print_solution(solution, title='First Part')

    print("Part 2 - Example")
    print("================")
    (games_with_rounds, game_maxes,
     game_powers, solution) = solver2('02/example1')

    print("\nEach Row a Game - Rounds in Format: (R,G,B)")
    print("===========================================")
    print_games(games_with_rounds)

    print("\nGame Maxes (R,G,B): ")
    print_game(game_maxes)

    print(f"Multiplied Game Maxes: {game_powers}")
    print()
    print_solution(solution, title='Second Example')

    print("Part 2 - Test")
    print("================")
    (games_with_rounds, game_maxes,
     game_powers, solution) = solver2('02/input')

    print("\nEach Row a Game - Rounds in Format: (R,G,B)")
    print("===========================================")
    print_games(games_with_rounds)

    print("\nGame Maxes (R,G,B): ")
    print_game(game_maxes)

    print(f"\nMultiplied Game Maxes:\n{game_powers}")
    print()
    print_solution(solution, title='Second Example')


if __name__ == "__main__":
    print("============= Day 02 - Cube Conundrum =============")
    main()
    print("================ Day 02 - Complete ================")