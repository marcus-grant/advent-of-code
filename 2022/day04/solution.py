#!/usr/bin/env python3

class ShipSectionsAssignment:
    def __init__(self, sections_str):
        self.ship_sections = ShipSectionsAssignment.sections_str_to_sections_list(sections_str)
        self.num_sections = len(self.ship_sections)
        self.first_section = self.ship_sections[0]
        self.last_section = self.ship_sections[self.num_sections - 1]

    def sections_str_to_sections_list(sections_str):
        """
        Given a string of two numbers seperated by a dash '-',
        this will create ShipSection objects of every contained section;
        starting with the number left of the dash (inclusive),
        and every section till the right number of the dash (inclusive).

        Parameters:
        section_str (string) of format "FIRST_SECTION-LAST_SECTION"

        Returns:
        A list of ShipSection objects of every ship section from & including
        the FIRST_SECTION to the left of the dash of sections_str,
        up to & including the LAST_SECTION number given on the right of the dash
        """
        # Split out the first and last sections of the sections string,
        # delimited by the '-' symbol
        first_section, last_section = sections_str.split('-')
        first_section, last_section = (int(first_section), int(last_section))

        # Create a list of sections to return
        sections_list = []
        # Loop through a range of first_section up to & including last_section
        for section_num in range(first_section, last_section + 1):
            # Add a ShipSection with the given number from the range
            sections_list.append(section_num)
        
        return sections_list
    
    def does_enclose_sections(self, sections):
        """
        Determines if a given set of sections are completely enclosed
        by this method's set of sections.
        That is, is every section given to this method present in self's sections

        Returns:
            (bool) if this set of sections completely enclose the given sections
        """
        if self.first_section <= sections.first_section:
            if self.last_section >= sections.last_section:
                return True
        return False
    
    def does_contain(self, section_num):
        if self.first_section <= section_num:
            if self.last_section >= section_num:
                return True
        return False
    
    def __str__(self):
        res = f"{self.first_section}-{self.last_section}"
        return res

        
    def __repr__(self):
        res = f"ShipSectionsAssignment('{self}')"
        return res

# assign = ShipSectionsAssignment('2-4')
# print(assign)

class ShipAssignmentPair:
    def __init__(self, ship_assignment_pair):
        first_of_pair, second_assignment = ship_assignment_pair.split(',')
        self.first_of_pair = ShipSectionsAssignment(first_of_pair)
        self.last_of_pair = ShipSectionsAssignment(second_assignment)
    
    def has_enclosed_sections(self):
        """
        Determines if one of the set of sections in the pair encloses the other.
        I.E. if one of the pair has every section of the other in its range.

        Returns:
        Boolean of whether one of the paired set of sections encloses the other.
        """
        if self.first_of_pair.does_enclose_sections(self.last_of_pair):
            return True
        if self.last_of_pair.does_enclose_sections(self.first_of_pair):
            return True
        return False
    
    def does_overlap(self):
        for section in self.first_of_pair.ship_sections:
            if self.last_of_pair.does_contain(section):
                return True
        return False

    def __repr__(self):
        pair_str = f"{self.first_of_pair},{self.last_of_pair}"
        res = f"ShipAssignmentPair({pair_str})"
        return res
    
    def __str__(self):
        res = f"({self.first_of_pair}, {self.last_of_pair})"
        return res
    
# pair = ShipAssignmentPair('2-4,6-8')
# print(pair)

class ShipAssignments:
    def __init__(self, assignments_file_path):
        self.file_path = assignments_file_path
        assignments = []
        try:
            with open(self.file_path) as file:
                for line in file:
                    # Remove any whitespace
                    pair_str = line.split()[0]
                    pair = ShipAssignmentPair(pair_str)
                    assignments.append(pair)
        except IOError as e:
            print(f"ShipAssignment file open error:\n{e}")
        except:
            print("Unkown Error during file ShipAssignment opening!")
        finally:
            self.assignments = assignments
            file.close()
    
    def read_ship_assignment_pairs_from_file(file):
        return assignments
    
    def get_enclosed_pairs(self):
        """
        Loops through every ship assignment pair and
        determines if one of the pairs of sections completely enclose the other.
        As in, if one of the pairs of sections completely contain the other's.

        Returns:
        A list of ShipAssignment pairs with
        one section in the pair enclosing the other.
        """
        enclosed_pairs = []
        for pair in self.assignments:
            if pair.has_enclosed_sections():
                enclosed_pairs.append(pair)
        return enclosed_pairs
    
    def count_enclosed_pairs(self):
        """
        Calls get_enclosed_sections to count
        how many pairs of sections enclose the other sections of the pair.

        Returns:
            The count of assignment pairs with
            one of the pair completely enclosing the other.
        """
        num_enclosed_sections = 0
        for pair in self.assignments:
            if pair.has_enclosed_sections():
                num_enclosed_sections += 1
        return num_enclosed_sections
    
    def get_overlapping_pairs(self):
        overlapping_pairs = []
        for pair in self.assignments:
            if pair.does_overlap():
                overlapping_pairs.append(pair)
        return overlapping_pairs
    
    def __str__(self):
        res = ''
        for pair in self.assignments:
            res = f"{res}\n{pair}"
        return res
    
    def __repr__(self):
        res = f"ShipAssignments({self.file_path})"
        return res

assignments = ShipAssignments('day4/input.txt')
print('Here are the ship assignments!')
print('==============================')
print(assignments)

print('These assigned pairs of sections enclose each other:')
print('====================================================')
enclosed_pairs = assignments.get_enclosed_pairs()
print(repr(enclosed_pairs))
print()
print(f"There are {assignments.count_enclosed_pairs()} enclosed sections pairs assigned")

print('These assigned pairs of sections overlap each other:')
print('====================================================')
overlapping_pairs = assignments.get_overlapping_pairs()
for pair in overlapping_pairs:
    print(pair)
print()
print(f"There are {len(overlapping_pairs)} overlapping pairs")



    
# Open file containing input for each elf rucksack seprated by blank newline
# with open("day3/input.txt") as file:
#     for item in file:
#         print()
#         # Split out the whitespace characters for each line including newline
#         # The result is a signle list representing each rucksack
#         rucksack = item.split()[0]
#         print(f"Current rucksack contains: {rucksack}")

#         # Split the rucksack evenly to represent each rucksack compartment
#         # ...but first check that the length of the rucksack is even
#         if len(rucksack) % 2 == 1:
#             # If it's odd, then something is wrong
#             print("ERROR: Something is wrong!")
#             print("Each compartment in the rucksack is supposed to have EXACTLY as many items.")
#             print("Skipping...")
#             break;
#         part1, part2 = (rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:])
#         print(f"part1: {part1}, part2: {part2}")
#         print(f"len1: {len(part1)}, len2: {len(part2)}")

#         # Add both compartments the rucksacks list
#         rucksacks.append((part1, part2))

# Here are the rucksacks
# print(rucksacks)

# Define a function to find the duplicate item for each compartment of a rucksack
# def find_rucksack_duplicates(rucksack):
#     print(f"Current Rucksack: {rucksack}")
#     matched_items = []
#     for item0 in rucksack[0]:
#         # print(f"Looking for duplicates to item {item0} in compartment 0:")
#         for item1 in rucksack[1]:
#             # print(f"\tChecking {item1}, {'MATCHED' if item0 == item1 else  'UNMATCHED'}!")
#             if item0 == item1:
#                 print(f"{item0} is in both compartments!")
#                 matched_items.append(item0)
#     return matched_items

# Create a priority score for each letter in order
# abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
#     'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# ABC = list(map(lambda x: x.upper(), abc))
# priorities_list = [*abc, *ABC]

# Loop through each comportment of each rucksack and find the duplicate items in each
# sum_of_priorities = 0
# While adding up the sum of priorities of items to be reorganized that appear in both compartments
# for rucksack in rucksacks:
#     print()
#     duplicate_item = find_rucksack_duplicates(rucksack)[0]

    # Get the index of the priorities_list to get the number of priority
    # priority = priorities_list.index(duplicate_item) + 1
    # print(f"Priority for item {duplicate_item} is {priority}")

    # Sum the priority for each rucksack
    # sum_of_priorities += priority
    # print(f"Current sum of priorities: {sum_of_priorities}")

# print()
# print("=== Sum of Priorities ===")
# print(sum_of_priorities)
# print()


        
# print("=== Part Two ===")

# rucksack_groups = []
# rucksack_group = []
# for i in range(len(rucksacks)):
#     rucksack_group.append([*rucksacks[i][0], *rucksacks[i][1]])
#     if i % 3 == 2:
#         rucksack_groups.append(rucksack_group)
#         rucksack_group = []

# def find_duplicate_in_group(group):
#     duplicate = ''
#     # First loop through first rucksack of group
#     for item0 in group[0]:
#         print()
#         print(f"item0: {item0}")
#         for item1 in group[1]:
#             print(f"\titem1: {item1}")
#             if item0 != item1:
#                 print(f"\t{item0} UNMATCHED with {item1}")
#                 print("\tSkipping to next item")
#                 continue
#             print(f"\t{item0} MATCHES {item1}")
#             print(f"\tChecking last rucksack of group using {item0}!")
#             for item2 in group[2]:
#                 print(f"\t\titem2: {item2}")
#                 if item1 != item2:
#                     print(f"\t\t{item1} UNMATCHED with {item2}")
#                     print("\t\tSkipping to next item")
#                     continue
#                 print(f"\t\t{item1} MATCHES {item2}")
#                 print("Found the duplicate!")
#                 duplicate = item0
#     return duplicate
                
                


# # print all rucksack groups
# sum_of_priorities = 0
# for group in rucksack_groups:
#     print()
#     for rucksack in group:
#         print(rucksack)
#     duplicate = find_duplicate_in_group(group)
#     priority = priorities_list.index(duplicate) + 1
#     sum_of_priorities += priority

# print(f"Sum of priorities: {sum_of_priorities}")
