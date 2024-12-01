import attrs
import dataclasses
import math
import random
from rich import print as rprint
from rich import console
import rich
import re
import time
from typing import Any, Optional, List, Tuple, Dict, Union
from typing import Literal, LiteralString, NewType

console = console.Console()
cprint = console.print

def print_solution(
        sol: str, title: str="", style: str="bold red", justify: str="center"
) -> None:
    msg = '[bold green]Solution'
    msg += f' to {title}[/bold green]' if len(title) > 0 else '[/bold green]'
    panel = rich.panel.Panel.fit(sol, title=msg, style="bold red")
    cprint(panel, justify=justify, new_line_start=True)

def print_panel(msg: str, title: str="",
                style: str="yellow", justify: str="center") -> None:
    title = None if len(title) == 0 else title
    panel = rich.panel.Panel.fit(msg, title=title, style=style)
    cprint(panel, justify=justify, new_line_start=True)

def read_input_lines(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines


class Card():
    @classmethod
    def _ten_to_ace_map(cls) -> list[str]: return ['T', 'J', 'Q', 'K', 'A']

    @classmethod
    def _char_to_rank(cls, rank_str: str) -> int:
        if len(rank_str) != 1:
            raise ValueError(f"Invalid rank: {rank_str}")
        rank_int = 0
        try:
            rank_int = int(rank_str)
            if rank_int < 2 or rank_int > 9:
                raise ValueError(f"Invalid rank: {rank_str}")
            return rank_int
        except ValueError:
            return cls._ten_to_ace_map().index(rank_str) + 10
    
    @classmethod
    def _rank_to_char(cls, rank_int: int) -> str:
        if not (2 <= rank_int <= 14):
            raise ValueError(f"Invalid rank: {rank_int}")
        if rank_int < 10:
            return str(rank_int)
        return cls._ten_to_ace_map()[rank_int - 10]

    @classmethod
    def _convert(cls, rank: Union[int, str]) -> int:
        if isinstance(rank, Card):
            return rank.rank
        if isinstance(rank, int):
            return rank
        if isinstance(rank, str):
            if len(rank) != 1:
                raise ValueError(f"Invalid rank length not 1: {rank}")
            return cls.char_to_rank(rank)
        raise ValueError(f"Invalid rank type: {type(rank)}")
    
    def __init__(self, rank: Union[int, str]):
        if isinstance(rank, int):
            self.rank = rank
            return
        if not isinstance(rank, str):
            raise ValueError(f"Invalid rank type: {type(rank)}")
        self.rank = self._char_to_rank(rank)
    
    def __str__(self) -> str: return self._rank_to_char(self.rank)

    def __repr__(self) -> str: return f"Card({self.__str__()})"

    def __eq__(self, other: any) -> bool: return self.rank == self._convert(other)
    
    def __gt__(self, other: any) -> bool: return self.rank > self._convert(other) 
    
    def __lt__(self, other: any) -> bool: return self.rank < self._convert(other)

    def __ge__(self, other: any) -> bool: return self.rank >= self._convert(other)

    def __le__(self, other: any) -> bool: return self.rank <= self._convert(other)

@attrs.define
class Hand:
    cards: list[Card] = attrs.field(default=[], init=False)
    def __init__(self, cards: Union[str, list[Union[Card, str]]]):
        self.cards = []
        if isinstance(cards, str):
            # Split the string into single characters
            self.cards = [Card(c) for c in cards.split()]
            return
        if not isinstance(cards, list):
            raise ValueError(f"Invalid type: {type(cards)}")
        for c in cards:
            if not isinstance(c, (Card, str)):
                raise ValueError(f"Invalid type: {type(c)}")
            if isinstance(c, Card):
                self.cards.append(c)
                continue
            self.cards.append(Card(c))
    
    def count_cards(self, cards: Optional[list[Card]] = None)-> dict[int, int]: # Returns dict of rank to count
        if cards is None: cards = self.cards
        card_count = {}
        ranks = [c.rank for c in cards]
        for r in ranks:
            card_count[r] = card_count.get(r, 0) + 1
        return card_count

    def get_dupe_card_sets(self) -> list[list[Card]]:
        # Returns list of set of dupe cards
        dupe_card_sets = []
        card_count = self.count_cards()
        for rank, count in card_count.items():
            if count > 1:
                dupe_card_sets.append([c for c in self.cards if c.rank == rank])
        return dupe_card_sets
    
    def get_max_dupe(self, counts: Optional[list[int, int]] = None) -> int:
        if counts is None:
            counts = max([len(s) for s in self.get_dupe_card_sets()])
        return max(counts)
    
    def single_cards_stronger(self, others: list[cards]) -> bool:
        for me, other in zip(self.cards, other):
            if me > other:
                return True
        return False
    
    def has_full_house(
            self, counts: Optional[dict[int, int]] = None, cards: list[Card] = []
    ) -> bool:
        active_cards = []
        if len(cards) > 0: active_cards = cards
        else: active_cards = self.cards
        if counts is None: counts = self.count_cards(active_cards)
        counts = list(counts.values())
        if 3 in counts and 1 in counts: return False
        return False

    def __eq__(self, others: list[Card]) -> bool:
        for me, other in zip(self.cards, other):
            if me != other:
                return False
        return True
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Hand): raise ValueError(f"Invalid type: {type(other)}")
        if self.__eq__(other): return False
        dupe_counts = (self.count_cards(), other.count_cards())
        max_dupes = (self.get_max_dupe(dupe_counts[0]),
                     other.get_max_dupe(dupe_counts[1]))
        if max_dupes[0] > max_dupes[1]: return True
        if max_dupes[0] < max_dupes[1]: return False
        if max_dupes[0] == max_dupes[1]:
            if max_dupes[0] == 3:
                me_full = self.has_full_house(dupe_counts[0])
                other_full = other.has_full_house(dupe_counts[1])
                if me_full and not other_full: return True
        return self.single_cards_stronger(other.cards)
    
    def __str__(self) -> str:
        return str(' '.join([str(c) for c in self.cards]))
    
    def __repr__(self) -> str:
        return f"Hand({''.join([str(c) for c in self.cards])})"

@attrs.define
class Game:
    game_str: str = attrs.field(default="")
    hand: Hand = attrs.field(init=False, default=Hand([]), kw_only=True)
    bet: int = attrs.field(default=0, kw_only=True)

    def _init_hand_str(self) -> None:
        self.hand = Hand(self.hand)
    
    def _init_hand_list(self) -> None:
        new_hand = []
        for c in self.hand:
            if isinstance(c, Card):
                new_hand.append(c)
                continue
            if isinstance(c, str):
                new_hand.append(Card(c))
                continue
            raise ValueError(f"Invalid type in init of list Hand: {type(c)}")

    def __attrs_post_init__(self):
        if len(self.game_str) > 0:
            self.hand = Hand(self.game_str.split(" ")[0].strip())
            self.bet =  int(self.game_str.split(" ")[1].strip())
            return
        if isinstance(self.hand, str): self._init_hand_str()
        if isinstance(self.hand, list): self._init_hand_list()
        if not isinstance(self.hand, Hand):
            raise ValueError(f"Invalid type: {type(self.hand)}")
    
    def __str__(self) -> str:
        return f"{self.hand.__repr__()}, bet={self.bet}"
    
    def __repr__(self) -> str:
        return f"Game({self.__str__()}))"
    
def part1(input_file: str) -> int:
    games = [Game(line) for line in read_input_lines(input_file)]
    for i, g in enumerate(games):
        hand = g.hand
        title = f'[yellow] Dealed Hand for Game #{i}[/yellow]'
        cards_str = f"\n[yellow]:Hand:\n{hand.cards}[/yellow]"
        dupes_str = "[g]:exclamation::exclamation:\n====\n[/g][bold red]"
        dupes = hand.duplicate_card_sets()
        for dupe_set in dupes:
            dupes_str += ' '.join(str(c) for c in dupe_set) + '\n'
        msg = cards_str + '\n[bold red]\n' + dupes_str
        print_panel(msg, title=title, style="green")

    return 0

def part2(input_file: str) -> int:
    lines = read_input_lines(input_file)

    return 0

def main():
    EXAMPLE = f"{DAY}/example.txt"
    INPUT = f"{DAY}/input.txt"
    TITLES = [ # Toggle these to control which parts of the code are run
        "Part One - EXAMPLE",
        # "Part One - INPUT",
        # "Part Two - EXAMPLE",
        # "Part Two - INPUT",
    ]
    for t in TITLES:
        print_panel(t, style="bold green")
        if 'one' in t.lower() or '1' in t.lower():
            if 'example' in t.lower():
                print_solution(f"{part1(EXAMPLE)}", title=t)
                continue
            print_solution(f"{part1(INPUT)}", title=t)
            continue
        if 'example' in t.lower():
            print_solution(f"{part2(EXAMPLE)}", title=t)
            continue
        print_solution(f"{part2(INPUT)}", title=t)
        

if __name__ == "__main__":
    DAY = "07"
    DAY_TITLE = "Camel Cards"
    msg = f"[bold green]Advent of Code - Day {DAY} - {DAY_TITLE} [/bold green]" 
    print_panel(msg ,style="bold red")
    main()
    msg = f"[bold red]Advent of Code - Day {DAY} - Complete![/bold red]" 
    print_panel(msg, style="bold green")
