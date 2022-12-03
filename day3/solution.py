#!/usr/bin/env python3

# Setup a list to hold all of the rock paper scissor round scores
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