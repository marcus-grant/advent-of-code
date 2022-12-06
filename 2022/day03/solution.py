#!/usr/bin/env python3

# Setup a list to hold all given rucksacks
rucksacks = []

# Open file containing input for each elf rucksack seprated by blank newline
with open("day3/input.txt") as file:
    for item in file:
        print()
        # Split out the whitespace characters for each line including newline
        # The result is a signle list representing each rucksack
        rucksack = item.split()[0]
        print(f"Current rucksack contains: {rucksack}")

        # Split the rucksack evenly to represent each rucksack compartment
        # ...but first check that the length of the rucksack is even
        if len(rucksack) % 2 == 1:
            # If it's odd, then something is wrong
            print("ERROR: Something is wrong!")
            print("Each compartment in the rucksack is supposed to have EXACTLY as many items.")
            print("Skipping...")
            break;
        part1, part2 = (rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:])
        print(f"part1: {part1}, part2: {part2}")
        print(f"len1: {len(part1)}, len2: {len(part2)}")

        # Add both compartments the rucksacks list
        rucksacks.append((part1, part2))

# Here are the rucksacks
# print(rucksacks)

# Define a function to find the duplicate item for each compartment of a rucksack
def find_rucksack_duplicates(rucksack):
    print(f"Current Rucksack: {rucksack}")
    matched_items = []
    for item0 in rucksack[0]:
        # print(f"Looking for duplicates to item {item0} in compartment 0:")
        for item1 in rucksack[1]:
            # print(f"\tChecking {item1}, {'MATCHED' if item0 == item1 else  'UNMATCHED'}!")
            if item0 == item1:
                print(f"{item0} is in both compartments!")
                matched_items.append(item0)
    return matched_items

# Create a priority score for each letter in order
abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ABC = list(map(lambda x: x.upper(), abc))
priorities_list = [*abc, *ABC]

# Loop through each comportment of each rucksack and find the duplicate items in each
sum_of_priorities = 0
# While adding up the sum of priorities of items to be reorganized that appear in both compartments
for rucksack in rucksacks:
    print()
    duplicate_item = find_rucksack_duplicates(rucksack)[0]

    # Get the index of the priorities_list to get the number of priority
    priority = priorities_list.index(duplicate_item) + 1
    print(f"Priority for item {duplicate_item} is {priority}")

    # Sum the priority for each rucksack
    sum_of_priorities += priority
    print(f"Current sum of priorities: {sum_of_priorities}")

print()
print("=== Sum of Priorities ===")
print(sum_of_priorities)
print()


        
print("=== Part Two ===")

rucksack_groups = []
rucksack_group = []
for i in range(len(rucksacks)):
    rucksack_group.append([*rucksacks[i][0], *rucksacks[i][1]])
    if i % 3 == 2:
        rucksack_groups.append(rucksack_group)
        rucksack_group = []

def find_duplicate_in_group(group):
    duplicate = ''
    # First loop through first rucksack of group
    for item0 in group[0]:
        print()
        print(f"item0: {item0}")
        for item1 in group[1]:
            print(f"\titem1: {item1}")
            if item0 != item1:
                print(f"\t{item0} UNMATCHED with {item1}")
                print("\tSkipping to next item")
                continue
            print(f"\t{item0} MATCHES {item1}")
            print(f"\tChecking last rucksack of group using {item0}!")
            for item2 in group[2]:
                print(f"\t\titem2: {item2}")
                if item1 != item2:
                    print(f"\t\t{item1} UNMATCHED with {item2}")
                    print("\t\tSkipping to next item")
                    continue
                print(f"\t\t{item1} MATCHES {item2}")
                print("Found the duplicate!")
                duplicate = item0
    return duplicate
                
                


# print all rucksack groups
sum_of_priorities = 0
for group in rucksack_groups:
    print()
    for rucksack in group:
        print(rucksack)
    duplicate = find_duplicate_in_group(group)
    priority = priorities_list.index(duplicate) + 1
    sum_of_priorities += priority

print(f"Sum of priorities: {sum_of_priorities}")
