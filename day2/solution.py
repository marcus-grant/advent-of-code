#!/usr/bin/env python3

# Setup a list to hold all of the rock paper scissor round scores
game_scores = []

OPPONENT_ROCK = 'A'
OPPONENT_PAPER = 'B'
OPPONENT_SCISSOR = 'C'
PLAYER_ROCK = 'X'
PLAYER_PAPER = 'Y'
PLAYER_SCISSOR = 'Z'

HAND_SIGN_STR_DICT = {
    OPPONENT_ROCK: "ROCK",
    PLAYER_ROCK: "ROCK",
    OPPONENT_PAPER: "PAPER",
    PLAYER_PAPER: "PAPER",
    OPPONENT_SCISSOR: "SCISSOR",
    PLAYER_SCISSOR: "SCISSOR",
}

HAND_POINTS_DICT = {
    OPPONENT_ROCK: 1,
    OPPONENT_PAPER: 2,
    OPPONENT_SCISSOR: 3,
    PLAYER_ROCK: 1,
    PLAYER_PAPER: 2,
    PLAYER_SCISSOR: 3,
}

MATCH_POINTS_WIN = 6
MATCH_POINTS_DRAW = 3
MATCH_POINTS_LOSE = 0

PLAYER_WINS_MATCH_DICT = {
    PLAYER_ROCK: {
        OPPONENT_ROCK: False,
        OPPONENT_PAPER: False,
        OPPONENT_SCISSOR: True,
    },
    PLAYER_PAPER: {
        OPPONENT_ROCK: True,
        OPPONENT_PAPER: False,
        OPPONENT_SCISSOR: False,
    },
    PLAYER_SCISSOR: {
        OPPONENT_ROCK: False,
        OPPONENT_PAPER: True,
        OPPONENT_SCISSOR: False,
    },
}

def play_round(player_hand, opponent_hand):
    round_score = HAND_POINTS_DICT[player_hand]
    player_hand_str = HAND_SIGN_STR_DICT[player_hand]
    opponent_hand_str = HAND_SIGN_STR_DICT[opponent_hand]
    print(f"Player plays {player_hand_str}\t- Opponent plays {opponent_hand_str}")
    print(f"{player_hand_str} is worth {round_score} points.")

    player_wins = PLAYER_WINS_MATCH_DICT[player_hand][opponent_hand]
    if not player_wins:
        if player_hand_str == opponent_hand_str:
            print(f"{player_hand_str} draws to {opponent_hand_str}! No extra points.")
            round_score += MATCH_POINTS_DRAW
        else:
            print(f"{player_hand_str} loses to {opponent_hand_str}! No extra points.")
            round_score += MATCH_POINTS_LOSE
    else:
        print(f"{player_hand_str} beats {opponent_hand_str}! Awarded 6 extra points.")
        round_score += MATCH_POINTS_WIN
    
    return round_score


# Open file containing input for each elf inventory seprated by blank newline
with open("day2/input.txt") as file:
    # Set counters for...
    # Each round's total score for the player vs opponent

    # Loop through each line in the file.
    # Each one is either a number of calories or...
    # ...a blank line w. only a newline to indicate end of an elf's inventory
    player_total_score = 0
    games_round_count = 0
    for item in file:
        # Current game round, removing all whitespace, including newline
        current_round = item.split()
        opponent_hand, player_hand = current_round[0], current_round[1]
        print(f"Current round of matches is #{games_round_count}")
        current_round_score = play_round(player_hand, opponent_hand)
        game_scores.append(current_round_score)
        player_total_score += current_round_score
        games_round_count += 1
        print(f"Player earns {current_round_score} points this round.")
        print(f"Player has a total score of {player_total_score} points so far.")
        print()

print("=== Part Two ===")
print("Correcting the understanding of the strategy guide...")
print("X: Means the player should pick the losing hand to the opponent")
print("Y: Means the player should pick the drawing hand to the opponent")
print("Z: Means the player should pick the winning hand to the opponent")

# Correction to guide for part 2
PLAYER_SHOULD_LOSE = 'X'
PLAYER_SHOULD_DRAW = 'Y'
PLAYER_SHOULD_WIN = 'Z'

PLAYER_SHOULD_EARN_THESE_POINTS = {
    PLAYER_SHOULD_LOSE: MATCH_POINTS_LOSE,
    PLAYER_SHOULD_DRAW: MATCH_POINTS_DRAW,
    PLAYER_SHOULD_WIN: MATCH_POINTS_WIN,
}

PLAYER_STRAT_STR_DICT = {
    PLAYER_SHOULD_LOSE: "LOSE",
    PLAYER_SHOULD_DRAW: "DRAW",
    PLAYER_SHOULD_WIN: "WIN",
}

PLAYER_STRAT_HAND_DICT = {
    PLAYER_SHOULD_LOSE: {
        OPPONENT_ROCK: PLAYER_SCISSOR,
        OPPONENT_PAPER: PLAYER_ROCK,
        OPPONENT_SCISSOR: PLAYER_PAPER,
    },
    PLAYER_SHOULD_DRAW: {
        OPPONENT_ROCK: PLAYER_ROCK,
        OPPONENT_PAPER: PLAYER_PAPER,
        OPPONENT_SCISSOR: PLAYER_SCISSOR,
    },
    PLAYER_SHOULD_WIN: {
        OPPONENT_ROCK: PLAYER_PAPER,
        OPPONENT_PAPER: PLAYER_SCISSOR,
        OPPONENT_SCISSOR: PLAYER_ROCK,
    },
}

def play_round_correctly(player_strat, opponent_hand):
    match_points = PLAYER_SHOULD_EARN_THESE_POINTS[player_strat]
    player_strat_str = PLAYER_STRAT_STR_DICT[player_strat]
    opponent_hand_str = HAND_SIGN_STR_DICT[opponent_hand]
    player_hand = PLAYER_STRAT_HAND_DICT[player_strat][opponent_hand]
    player_hand_score = HAND_POINTS_DICT[player_hand]
    player_hand_str = HAND_SIGN_STR_DICT[player_hand]
    total_round_score = match_points + player_hand_score

    print(f"Player should {player_strat_str} to {opponent_hand_str}, therefore...")
    print(f"Player plays {player_hand_str}\t- Opponent plays {opponent_hand_str}")
    print(f"Player earns {player_hand_score} points for playing {player_hand_str}")
    print(f"Player earns {match_points} points for the {player_strat_str}")

    return total_round_score


# Open file containing input for each elf inventory seprated by blank newline
with open("day2/input.txt") as file:
    # Set counters for...
    # Each round's total score for the player vs opponent

    # Loop through each line in the file.
    # Each one is either a number of calories or...
    # ...a blank line w. only a newline to indicate end of an elf's inventory
    player_total_score = 0
    games_round_count = 0
    for item in file:
        # Current game round, removing all whitespace, including newline
        current_round = item.split()
        opponent_hand, player_strat = current_round[0], current_round[1]
        print(f"Current round of matches is #{games_round_count}")
        current_round_score = play_round_correctly(player_strat, opponent_hand)
        player_total_score += current_round_score
        games_round_count += 1
        print(f"Player earns {current_round_score} points this round.")
        print(f"Player has a total score of {player_total_score} points so far.")
        print()