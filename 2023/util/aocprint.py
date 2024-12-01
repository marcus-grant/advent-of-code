from colorama import Fore, Back, Style

def print_solution(sol: str, title: str=''):
    s = f"{Back.GREEN}{Style.BRIGHT}Solution"
    if len(title) > 0:
        s += f" to {title}"
    s += f"{Style.RESET_ALL}: {Fore.LIGHTMAGENTA_EX}{sol}{Style.RESET_ALL}"
    print(s)