# from attrs import asdict, define, make_class, Factory, field
# from attrs import asdict, define, make_class, Factory, field
# from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
# from colorama import Fore, Back, Style
import re
import time
from rich import print as rprint
import rich

def print_solution(sol: str, title: str=""):
    rprint(f"[b u red]Solution to {title}:[b u green]    {sol}    ")

def read_input(input_file_path: str) -> list[str]:
    with open(input_file_path, "r") as f:
        lines = f.read().splitlines()
    return lines

class ScratchCard():
    def process_card_str(card_str: str) -> Tuple[int, list[int], list[int]]:
        # Sample string
        # "Card     5 :   1 20 3 40 5 |   99 1   71    401 33 40 34 5 "
        # |only this^ | win_nums(all) |  scratch_nums(all)(only \d+)  |
        # Extract the card ID using regex
        card_id, card_str = re.split(r"Card\s*(\d+)", card_str)[1:]
        card_id = int(card_id.strip())

        # Split remaining card_str by pipe (|) left = win #s, right = scratch #s
        win_nums, scratch_nums = card_str.split('|')
        win_nums = win_nums.split(':')[-1].strip()
        win_nums = [
            int(s.strip()) for s in re.split(r"\s+", win_nums) if len(s) > 0]
        scratch_nums = [
            int(s.strip()) for s in re.split(r"\s+", scratch_nums) if len(s) > 0
        ]
        return (card_id, win_nums, scratch_nums)
            
    def __init__(
            self,
            id: Optional[int]=None,
            win_nums: [list[int]]=[],
            scr_nums: [list[int]]=[],
            card_str: Optional[str]=None,
            calc_props: bool=True,
    ):
        # Initialize the cached calculated properties
        self._matches = None
        self._wins = None
        self._winnings = None
        self._win_ids = None
        self._copied_from = None
        if card_str is None:
            # Validate the input is not None
            assert id is not None
            self.id = id
            self.winning_nums = win_nums
            self.scratch_nums = scr_nums
        else:
            # Process the card string
            self.id, self.winning_nums, self.scratch_nums = (
                ScratchCard.process_card_str(card_str)
            )
        if calc_props:
            self.update_calculated_properties()
    
    def matches(self) -> list[int]:
        if self._matches is None:
            self._matches = []
        if len(self._matches) > 0:
            return self._matches
        for n in self.winning_nums:
            if n in self.scratch_nums:
                self._matches.append(n)
        return self._matches
    
    def wins(self) -> int:
        if self._wins is None:
            self._wins = len(self.matches())
        return self._wins
    
    def winnings(self) -> int:
        if self._winnings is None:
            self._winnings = 0
            if self.wins() > 0:
                self._winnings = 1 << (self.wins() - 1)
        return self._winnings
    
    def card_ids_won(self) -> list[int]:
        if self._win_ids is None:
            self._win_ids = [self.id + i + 1 for i in range(self.wins())]
        return self._win_ids
    
    def update_calculated_properties(self) -> None:
        _ = self.matches()
        _ = self.wins()
        _ = self.winnings()
        _ = self.card_ids_won()
    
    def stringify_nums_with_matches(self, nums: list[int]) -> str:
        s = ' '.join(map(str, nums))
        for m in self.matches():
            ms = str(m)
            pattern = r"\b" + re.escape(ms) + r"\b"
            s = re.sub(pattern, f"[b u red]{ms}[/b u red]", s)
        return s

    def stringify_win_nums(self, with_matches: bool=False) -> str:
        if not with_matches:
            return ' '.join(map(str, self.winning_nums))
        return self.stringify_nums_with_matches(self.winning_nums)
    
    def stringify_scratch_nums(self, with_matches: bool=False) -> str:
        if not with_matches:
            return ' '.join(map(str, self.scratch_nums))
        return self.stringify_nums_with_matches(self.scratch_nums)
    
    def stringify(self, with_matches=True) -> str:
        id_str = f"{self.id}"
        win_str = self.stringify_win_nums(with_matches, with_matches)
        scratch_str = self.stringify_scratch_nums(with_matches, with_matches)
        return f"C#:{id_str}, W#s:{win_str} | {scratch_str}"
    
    def __str__(self) -> str:
        return self.stringify()
    
    def __repr__(self):
        return self.stringify()

class ScratchCardTable():
    def __init__(self, input_file: str, show_progress=True, delay: float=0.0):
        input_lines = read_input(input_file)
        self.cards: list[ScratchCard] = []
        self._cards_redeemed: list[ScratchCard] = []
        if not show_progress:
            for card_str in input_lines:
                card = ScratchCard(card_str=card_str)
                self.cards.append(card)
        else:
            from rich.progress import track
            count = len(input_lines)
            desc = f"Processing {count} ScratchCards..."
            for ci in track(range(count), description=desc):
                card = ScratchCard(card_str=input_lines[ci])
                self.cards.append(card)
                time.sleep(delay)
            print()

    def print_table(self, part: int=1):
        from rich.table import Table
        table = Table(show_header=True, header_style="bold green")
        table.add_column("CardID")
        table.add_column("Winning #s")
        table.add_column("Scratch #s")
        table.add_column("Ws")
        if part == 1:
            table.add_column("$")
        if part == 2:
            table.add_column("Won Cards")

        for card in self.cards:
            winning_nums = card.stringify_win_nums(with_matches=True)
            scratch_nums = card.stringify_scratch_nums(with_matches=True)

            win_cell = '' # Conditional on part 1 or 2 (diff win info)
            if part == 1:
                win_cell = str(card.winnings())
            if part == 2:
                win_cell = ' '.join(map(str, card.card_ids_won()))
            table.add_row(
                str(card.id),
                winning_nums,
                scratch_nums,
                str(card.wins()),
                str(win_cell),
            )
        rprint(table)
    
    def copy_card(self, card: ScratchCard, copied_from: int) -> ScratchCard:
        new_card = ScratchCard(
            id=card.id,
            win_nums=card.winning_nums,
            scr_nums=card.scratch_nums,
            calc_props=False,
        )
        new_card._copied_from = copied_from
        new_card._matches = card._matches
        new_card._wins = card._wins
        new_card.card_ids_won = card.card_ids_won
        return new_card
    
    def redeem_card(self, card_id: int, copied_from) -> ScratchCard:
        for card in self.cards:
            if card.id == card_id:
                return self.copy_card(card, copied_from)
        raise ValueError(f"Could not find card with id {card_id}")
    
    def redeem_cards(self, debug: bool=False) -> None:
        from rich.progress import Progress
        # First redeem all original cards
        self._cards_redeemed.extend(self.cards)
        # Keep going through the redeemed cards until no more copies are made
        with Progress() as progress:
            redeem_idx = 0
            task = progress.add_task("[cyan]Redeeming cards...",
                                     total=len(self._cards_redeemed))
            while redeem_idx < len(self._cards_redeemed):
                card = self._cards_redeemed[redeem_idx]
                if debug:
                    print((f"Redeeming cards for {card.id}, " +
                           f"copied from {card._copied_from}"))
                if card.wins() > 0:
                    for card_id_to_redeem in card.card_ids_won():
                        new_card = self.redeem_card(card_id_to_redeem, card.id)
                        self._cards_redeemed.append(new_card)
                        debug and print(f"    Redeemed card {new_card.id}")
                redeem_idx += 1
                desc = (f"[cyan]Redeeming "
                        + f"({redeem_idx}/{len(self._cards_redeemed)})"
                        + ' cards....[/cyan]')
                progress.update(
                    task,
                    advance=1,
                    total=len(self._cards_redeemed),
                    description=desc
                )
        progress.update(task,
                        advance=card.wins(),
                        completed=len(self._cards_redeemed),
                        description=f"Redeeming {len(self._cards_redeemed)} cards... Done!")

def part1(input_file: str) -> int:
    delay = 0.005 if 'input' in input_file else 0.2
    card_table = ScratchCardTable(input_file, show_progress=True, delay=delay)

    rprint("[green]Here are the scratch cards with matches & winnings:[/green]")
    print()
    card_table.print_table()

    print()
    return sum([c.winnings() for c in card_table.cards])

def part2(input_file: str) -> int:
    delay = 0.05 if 'input' in input_file else 0.2
    card_table = ScratchCardTable(input_file, show_progress=True, delay=delay)

    rprint("[green]Here are the scratch cards with matches & winnings:[/green]")
    print()
    card_table.print_table(part=2)

    card_table.redeem_cards()
    if len(card_table._cards_redeemed)  < 100000:
        print('Redeemed Cards:')
        print([c.id for c in card_table._cards_redeemed])
        print()
    print()

    return len(card_table._cards_redeemed)

def main():
    EXAMPLE = "04/example.txt"
    INPUT = "04/input.txt"

    print()
    print("Part One - Example")
    print("==================")

    print()
    solution = part1(EXAMPLE)
    print_solution(f"{solution}", title="Part One (Example)")

    print()
    print("Part One - Input")
    print("================")

    print()
    solution = part1(INPUT)
    print_solution(f"{solution}", title="Part One (INPUT)")

    print()
    print("Part Two - Example")
    print("==================")

    print()
    solution = part2(EXAMPLE)
    print_solution(f"{solution}", title="Part Two (Example)")

    print()
    print("Part Two - Input")
    print("================")

    print()
    solution = part2(INPUT)
    print_solution(f"{solution}", title="Part Two (Example)")
    print()


if __name__ == "__main__":
    print('==================== Day 04 - Scratchcards =====================')
    main()
    print('====================== Day 04 - Complete =======================')

