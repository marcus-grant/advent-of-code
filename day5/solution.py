#!/usr/bin/env python3

class CrateStack:
    def __init__(self, crate_stack_list):
        self.stack = []
        self.count = 0
        for crate_id in crate_stack_list:
            self.push(crate_id)
    
    def push(self, crate_id):
        if not crate_id == ' ':
            self.stack.append(crate_id)
            self.count += 1
    
    def pop(self):
        if self.count <= 0:
            return None
        popped_crate = self.stack.pop()
        self.count -= 1
        return popped_crate
    
    def pop_multiple(self, amount):
        popped_crates = []
        for _ in range(amount):
            popped_crates.append(self.pop())
        popped_crates.reverse()
        return popped_crates
    
    def peek(self):
        res = self.stack[self.count - 1]
        return res

    def __str__(self):
        return str(self.stack)
        
    def __repr__(self):
        res = 'CrateStack(['
        for crate_id in self.stack:
            res = f"{res}'{crate_id}',"
        res = res[:-1]
        res += '])'
        return res

# cratestack = CrateStack(['A', 'B', 'C'])
# print(cratestack)
# print(repr(cratestack))

class CrateStacks:
    def __init__(self, crate_stack_drawing):
        # First split the crate_stack_drawing into its lines
        stacks_lines = crate_stack_drawing.split('\n')

        # The legend indicating the number of stacks and their horizontal position
        # The index of that line is going to be -2 from len bc there's an empty line at the end
        stacks_legend_idx = len(stacks_lines) - 2
        stacks_legend = stacks_lines[stacks_legend_idx]

        # Now loop through the stacks legend line to get the text column indeces of the crates above
        horiz_crate_positions = []
        for i in range(len(stacks_legend)):
            if not stacks_legend[i] == ' ':
                horiz_crate_positions.append(i)

        # Now get the number of crate stacks using the last number in the stacks_legend
        self.num_stacks = int(stacks_legend[horiz_crate_positions[len(horiz_crate_positions) - 1]])

        # Then create the list of CrateStacks that will store all stacks in drawing
        self.stacks = []
        for i in range(self.num_stacks):
            self.stacks.append(CrateStack([]))
        
        # Now go from the bottom of the drawing lines, after the legend line,
        # and push new crates into the stacks
        for i in range(stacks_legend_idx - 1, -1, -1):
            # Then go through each line, using the horiz_crate_positions,
            # Extract the crate ids to be pushed into each stack
            current_crates_line = stacks_lines[i]
            crates_to_stack = []
            for j in horiz_crate_positions:
                crates_to_stack.append(current_crates_line[j])
            
            # Stack the crates by pushing the new crates to each stack
            # If they're empty, a spacebar is used as it appears in the drawing for crate_id
            stack_idx = 0
            for crate_id in crates_to_stack:
                self.stacks[stack_idx].push(crate_id)
                stack_idx += 1
    
    def __getitem__(self, idx):
        i = idx - 1
        res = self.stacks[i]
        return res
    
    def peek_all_stacks(self):
        peeks = []
        for stack in self.stacks:
            peeks.append(stack.peek())
        return peeks
        
    def __str__(self):
        res = ''
        stack_idx = 1
        for stack in self.stacks:
            res = f"{res}Stack#{stack_idx}: {stack}\n"
            stack_idx += 1
        return res


# crates_str =  '    [D]   \n'
# crates_str += '[N] [C]    \n'
# crates_str += '[Z] [M] [P]\n'
# crates_str += ' 1   2   3 \n'
# cratestacks = CrateStacks(crates_str)
# print(cratestacks)

class CraneInstruction:
    def __init__(self, instruction_str):
        instruction_nums = [int(s) for s in instruction_str.split() if s.isdigit()]
        self.amount = instruction_nums[0]
        self.src_stack = instruction_nums[1]
        self.dst_stack = instruction_nums[2]
    
    def __str__(self):
        res = f"{self.amount} x ({self.src_stack} => {self.dst_stack})"
        return res
    
    def __repr__(self):
        res = f"CraneInstruction('move {self.amount} from {self.src_stack} to {self.dst_stack}')"
        return res

# crane_instruct = CraneInstruction("move 1 from 2 to 3")
# print(crane_instruct)
# print(repr(crane_instruct))

class CraneOperator:
    def __init__(self, file_path, move_multiple_crates=False):
        self.file_path = file_path
        self.instructions = []
        self.num_instructions = 0
        crates_drawing_lines = []
        drawing_done = False
        self.move_multiple_crates = move_multiple_crates
        try:
            with open(self.file_path) as file:
                for line in file:
                    if line == '\n':
                        drawing_done = True
                    elif drawing_done:
                        self.instructions.append(CraneInstruction(line))
                        self.num_instructions += 1
                    else:
                        crates_drawing_lines.append(line)
        except IOError as e:
            print(f"InstructionManual file open error:\n{e}")
        except:
            print("Unkown Error during InstructionManual file opening!")
        finally:
            crates_str = ''
            for line in crates_drawing_lines:
                crates_str += line
            self.crate_stacks = CrateStacks(crates_str)
            file.close()
    
    def get_instruction_of_index(self, idx):
        res = self.instructions[idx]
        return res;
    
    def move_single_crates(self, instruction):
        for _ in range(instruction.amount):
            src_stack = self.crate_stacks[instruction.src_stack]
            dst_stack = self.crate_stacks[instruction.dst_stack]
            popped_crate = src_stack.pop()
            dst_stack.push(popped_crate)
    
    def move_multiple_crates_with_instructions(self, debug=False):
        for instruction in self.instructions:
            src = instruction.src_stack
            dst = instruction.dst_stack
            amount = instruction.amount
            popped_crates = self.crate_stacks[src].pop_multiple(amount)
            for crate in popped_crates:
                self.crate_stacks[dst].push(crate)
            if debug:
                print()
                print(instruction)
                print('======================')
                print(self.crate_stacks)
    
    def move_crates_till_instruction_num(self,
                                            instruction_num=None,
                                            debug=False):
        if not instruction_num:
            instruction_num = self.num_instructions
        for instruction_idx in range(instruction_num):
            instruction = self.instructions[instruction_idx]
            self.move_single_crates(instruction)
            if debug:
                print()
                print(instruction)
                print('======================')
                print(self.crate_stacks)
    
    def peek_all_stacks(self):
        res = self.crate_stacks.peek_all_stacks()
        return res

    
    def __len__(self):
        res = self.num_instructions
        return self.num_instructions
    


op = CraneOperator('day5/input.txt')
print()
print("The last instruction line from the manual file is:")
print(op.get_instruction_of_index(len(op) - 1))

print()
print("Time to execute all crane move opetions")
print("Current State of Stacks")
print("=======================")
print(op.crate_stacks)
op.move_crates_till_instruction_num(debug=True)

print()
print('The tops of every stack (in order) are:')
print('=======================================')
tops_of_stacks = op.peek_all_stacks()
print(tops_of_stacks)

print()
print("Time to execute all crane move operations (this time with multiple crates)")
print("Current State of Stacks")
print("=======================")
print(op.crate_stacks)
op = CraneOperator('day5/input.txt')
op.move_multiple_crates_with_instructions(debug=True)

print()
print('The tops of every stack (in order) are:')
print('=======================================')
tops_of_stacks = op.peek_all_stacks()
print(tops_of_stacks)

