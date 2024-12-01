from rich.console import Console

cprint = Console().print

def read_lines(file):
    with open(file) as input_file:
        return input_file.read().splitlines()

def parse_instruction(line: str) -> tuple[int, int]:
    """ Parse a string into an instruction tuple.
        The instruction string is separated by whitespace between
        the opartion (left) and the operand (right).
        Instructions:
            noop    -> 0
            addx op -> 1
    """
    ops = line.split(' ')
    opcode = 1 if ops[0].strip() == 'addx' else 0
    operand = int(ops[1].strip()) if len(ops) > 1 else 0
    return (opcode, operand)

def noop(*args) -> None:
    return

def addx(rd_a, rd_x, wr_x) -> None:
    wr_x(rd_a() + rd_x())

def decode_instruction(instr: tuple[int, int]) -> list[tuple]:
    opc, opd = instr[0], instr[1]
    funcs = [(noop, 0)]
    if opc == 1:
        funcs.append((addx, opd))
    return funcs

def create_registers(names: list[str]) -> tuple:
    registers = {}
    for name in names:
        registers[name] = 0
    
    def read_register(name: str) -> int:
        return registers[name]
    
    def write_register(name: str, value: int) -> None:
        if name not in registers:
            raise Exception(f'Invalid register name: {name}. Registers can only be created by factory function.')
        registers[name] = value
    return read_register, write_register

def run_cpu(
        instrs: list[tuple[int, int]],
        registers,
        max_cycles: int = 100000
) -> int:
    """ Run a CPU with the given instructions, registers, and output function.
    """
    # Create registers & set initial values
    reg_read, reg_write = registers(['x', 'p', 'a', 's'])
    reg_write('s', 0)
    reg_write('a', 0)
    reg_write('p', 0)
    reg_write('x', 1)
    loaded_instrs = [(noop, 0)]
    cycle = 0 # 0 indexed, 'i' register is the instruction pointer 1 indexed

    cycle_signals = set([40*i + 20 for i in range(int((20 + len(instrs)) / 40))])
    def alu() -> None:
        reg_write('a', loaded_instrs[reg_read('p')][1])
        regs = (lambda: reg_read('a'),
                lambda: reg_read('x'), lambda x: reg_write('x', x))
        loaded_instrs[reg_read('p')][0](*regs)
        reg_write('p', reg_read('p') + 1)

    while reg_read('p') < len(instrs) and cycle < max_cycles:
        # load instruction function from program memory (instrs) to instruction register (inst_fns)
        for i in decode_instruction(instrs[reg_read('p')]):
            loaded_instrs.append(i)
        # run alu one cycle
        alu()
        if cycle in cycle_signals:
            reg_write('s', reg_read('s') + (reg_read('x') * cycle))
            cprint(f'cycle: {cycle}, p: {reg_read("p")}, x: {reg_read("x")}, s: {reg_read("s")}')
        cycle += 1
    return reg_read('s')


def main():
    lines = read_lines('old/10/input.txt')
    instrs = [parse_instruction(line) for line in lines]
    addxs = len([i for i in instrs if i[0] == 1])
    cprint(instrs)
    out_cycles = set([40 * i + 20 for i in range(addxs+len(instrs))])
    signals_sum = 0
    cprint(run_cpu(instrs, create_registers), style='bold red')

if __name__ == '__main__':
    main()
