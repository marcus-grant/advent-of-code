from typing import List, Optional, Union, Callable, Iterable
from typing_extensions import Self
from rich import print

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 95437
        self.test2 = 24933642
        self.part1 = 0
        self.part2 = 0
    
    def parse(self, instr: str) -> List:
        # Make each line part of a list
        # And each item is another list for every command arg in the terminal IO
        self.data = [list(line.split(' ')) for line in instr.splitlines()]
        # Convert the solver data into [InterpretedCmd] list of objects
        self.data = [InterpretedCmd(cmd_list) for cmd_list in self.data]
    
    def solve(self):
        # Part 1 assuming '$ cd /' is the first command, it is in testcases
        # Build filesystem needed for both parts
        root = Directory('/', None, None)
        pwd = root
        for i in range(1, len(self.data)):
            cli: InterpretedCmd = self.data[i]
            if cli.is_cmd:
                if cli.cmd == 'cd':
                    d = pwd.cd(cli.args[0])
                    if not d is None:
                        pwd = d
                    else:
                        print(f"[red]ERROR[/red]: Directory {cli.args[0]} does not exist!")
                        print(f"Current directory: {pwd.name}")
            else:  # Then it is a stdout line
                if cli.stdout[0] == 'dir':
                    pwd.mkdir(cli.stdout[1])
                elif cli.stdout[0].isnumeric():
                    pwd.touch(cli.stdout[1], cli.stdout[0])

        # Now determine the sum of directories with total size less than 100k
        subdirs = root.get_subdirs_recursive()
        for d in subdirs:
            dsize = d.get_cumulitive_size_recursive()
            if dsize <= 100000:
                self.part1 += dsize
        
        # Part2: Determine the smallest directory to delete that would free up enough space
        # Part2: Also, what size is that directory.
        # Part2: Filesystem size is 70000000 or 70M, freespace needed 30000000 or 30M
        fs_size = 70000000
        space_needed = 30000000
        free_space = fs_size - root.get_cumulitive_size_recursive()
        subdir_sizes = [d.get_cumulitive_size_recursive() for d in subdirs]
        subdir_sizes.append(root.get_cumulitive_size_recursive())
        subdir_sizes.sort()
        for dsize in subdir_sizes:
            if free_space + dsize >= space_needed:
                self.part2 = dsize
                break
        

class InterpretedCmd:
    def __init__(self, cmd_list: List[str]):
        self.cmd_list = cmd_list
        self.is_cmd = True if cmd_list[0] == '$' else False
        self.cmd = None
        if self.is_cmd:
            self.cmd = cmd_list[1]
        self.args = None
        if len(cmd_list) > 2:
            self.args = cmd_list[2:]
        self.stdout = None
        if not self.is_cmd:
            self.stdout = cmd_list
    
    def __repr__(self):
        return f"InterpretedCmd({self.cmd_list})"

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def size_reducer(fsize_acc: int, f: Self) -> int:
        size = fsize_acc + f.size
        return size
    
    def __repr__(self) -> str:
        return f"File({self.name},{self.size})"


def reduce(fn: Callable, iterable: Iterable):
    accumulator = None
    for item in iterable:
        accumulator = fn(accumulator, item)
    return accumulator

class Directory:
    CONTENTS_TYPE = Optional[List[Union[Self, File]]]
    def __init__(self,
        name: str,
        parent: Optional[Self],
        contents: Optional[List[Union[Self, File]]]):

        self.name = name
        self.parent = parent
        self.contents = contents
    
    def is_empty(self):
        return not self.contents
    
    def get_files(self) -> List[File]:
        files = []
        for x in self.contents:
            if isinstance(x, File):
                files.append(x)
        return files
    
    def has_fname(self, fname: str) -> bool:
        files = self.get_files()
        for file in files:
            if file.name == fname:
                return True
        return False

    def get_dirs(self) -> List[Self]:
        dirs = []
        for x in self.contents:
            if isinstance(x, Directory):
                dirs.append(x)
        return dirs
    
    def has_dname(self, dname: str) -> bool:
        dirs: List[Self] = self.get_dirs()
        for d in dirs:
            if d.name == dname:
                return True
        return False
    
    def cd(self, dname: str) -> Optional[Self]:
        if dname == '..':
            return self.parent
        for d in self.get_dirs():
            if d.name == dname:
                return d
        return None

    def mkdir(self, dname: str):
        d = Directory(dname, self, None)
        if self.is_empty():
            self.contents = []
        if not self.has_dname(dname):
            self.contents.append(d)
    
    def touch(self, fname: str, fsize: str):
        fsize = int(fsize)
        f = File(fname, fsize)
        if self.is_empty():
            self.contents = []
        if not self.has_fname(fname):
            self.contents.append(f)
    
    def get_subdirs_recursive(self) -> List[Self]:
        subdirs = []
        queue: List[Self] = []
        queue.append(self)
        while queue:
            pwd = queue.pop(0)
            for d in pwd.get_dirs():
                if not d in subdirs:
                    queue.append(d)
                    subdirs.append(d)
        return subdirs
    
    def get_cumulitive_size(self):
        files = self.get_files()
        fsizes = [f.size for f in files]
        total_size = sum(fsizes)
        return total_size
    
    def get_cumulitive_size_recursive(self) -> int:
        # First do the files in this dir
        total_size = self.get_cumulitive_size()
        # Then get all subdirs and get their file sizes
        subdirs = self.get_subdirs_recursive()
        for d in subdirs:
            total_size += d.get_cumulitive_size()
        return total_size

    
    def __repr__(self):
        return f"Directory({self.name},{self.parent},{self.contents})"


