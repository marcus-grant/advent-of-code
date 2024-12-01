# A pretty printing library
from colorama import Fore, Back, Style

def get_colorized_round(rnd: tuple[int, int, int]) -> str:
    s = ''
    r, g, b = rnd
    PAREN_OPEN  = f"{Style.RESET_ALL}("
    PAREN_CLOSE = f"{Style.RESET_ALL})"
    COMMA       = f"{Style.RESET_ALL}, "
    s += PAREN_OPEN
    if rnd[0] > 0:
        s += f"{Fore.RED}{r}"
    else:
        s += f"{Fore.RESET}{r}"
    s += COMMA
    if rnd[1] > 0:
        s += f"{Fore.GREEN}{g}"
    else:
        s += f"{Fore.RESET}{g}"
    s += COMMA
    if rnd[2] > 0:
        s += f"{Fore.BLUE}{b}"
    else:
        s += f"{Fore.RESET}{b}"
    s += f"{PAREN_CLOSE}"
    return s

def get_colorized_game(game: list[tuple[int, int, int]]):
    colorized_rounds = [get_colorized_round(rnd) for rnd in game]
    colorized_rounds = ', '.join(colorized_rounds)
    return f"{Style.RESET_ALL}[{colorized_rounds}]{Style.RESET_ALL}"

def print_game(game: list[tuple[int, int, int]]):
    print(get_colorized_game(game))

def print_games(games: list[list[tuple[int, int, int]]]):
    for game in games:
        print_game(game)

def print_solution(sol: str, title: str=''):
    s = f"{Back.GREEN}{Style.BRIGHT}Solution"
    if len(title) > 0:
        s += f" to {title}"
    s += f"{Style.RESET_ALL}: {Fore.LIGHTMAGENTA_EX}{sol}{Style.RESET_ALL}"
    print(s)
