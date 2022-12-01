#!/usr/bin/env python3

# Setup array of total food item calories each elf is carrying
elf_inventories = []

# Open file containing input for each elf inventory seprated by blank newline
with open("input.txt") as file:
    # Set counters for...
    # current elf calories, current elf number, current item number
    elf_calories_carried = 0
    elf_num = 0
    item_num = 0

    # Loop through each line in the file.
    # Each one is either a number of calories or...
    # ...a blank line w. only a newline to indicate end of an elf's inventory
    for item in file:
        # Current item calories by removing all whitespace, including newline
        current_calories = ''.join(item.split())

        # If the result is number, then it's a valid item calory count
        if current_calories.isnumeric():
            print(f"Item #{item_num} with {current_calories}\tcalories")
            elf_calories_carried += float(current_calories)
            # Increment the item count
            item_num += 1
        # If not numberic, then probably a blank line is encountered
        # So end the count of current elf calories and prepare new elf count
        else:
            print(f"Elf #{elf_num} has {elf_calories_carried}\tcalories")
            print()
            elf_inventories.append(elf_calories_carried)

            # Reset calories_carried & item_num counters
            elf_calories_carried = 0
            item_num = 0
            # Increment elf_num counter
            elf_num += 1
            print(f"Looking at Elf #{elf_num}'s backpack:")

# Now with a list of elf carried calories, find the max
elf_carrying_most_calories = 0
elf_max_calories = elf_inventories[0]
print()
for elf_num in range(len(elf_inventories)):
    current_elf_cals = elf_inventories[elf_num]
    print(f"Elf #{elf_num} is carrying {current_elf_cals}cals.")
    if current_elf_cals > elf_max_calories:
        print("Elf #{elf_num} is now the elf carrying the most calories.")
        elf_carrying_most_calories = elf_num
        elf_max_calories = current_elf_cals
    else:
        print(f"Elf #{elf_num} is not carrying more than {elf_carrying_most_calories}.")
    print()

print()
print("========================================")
print("The elf carrying the most calories is...")
print(f"Elf #{elf_carrying_most_calories}, who has {elf_max_calories}calories.")
