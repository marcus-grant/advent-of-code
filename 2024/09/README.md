# Day 09 - Disk Fragmenter

## Part One

Another push of the button leaves you in
the familiar hallways of some friendly [amphipods][aoc-yr21-day23]!
Good thing you each somehow got your own personal mini submarine.
The Historians jet away in search of the Chief,
mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things,
you notice an amphipod in the corner struggling with his computer.
He's trying to make more contiguous free space by compacting all of the files,
but his program isn't working; you offer to help.

He shows you the **disk map** (your puzzle input) he's already generated.

**For example:**

```plaintext
2333133121414131402
```

The disk map uses a dense format to
represent the layout of **files** and *free space* on the disk.
The digits alternate between indicating the length of a file and
the length of free space.

So, a disk map like `12345` would represent a one-block file,
two blocks of free space, a three-block file, four blocks of free space,
and then a five-block file.
A disk map like `90909` would represent three nine-block files in a row
(with no free space between them).

Each file on disk also has an **ID number** based on the order of
the files as they appear **before** they are rearranged, starting with ID `0`.
So, the disk map `12345` has three files:
a one-block file with ID `0`, a three-block file with ID `1`,
and a five-block file with ID `2`.
Using one character for each block where digits are the file ID and
`.` is free space, the disk map `12345` represents these individual blocks:

```plaintext
0..111....22222
```

The first example above, `2333133121414131402`, represents these individual blocks:

```plaintext
00...111...2...333.44.5555.6666.777.888899
```

The amphipod would like to **move file blocks one at a time** from
the end of the disk to the leftmost free space block
(until there are no gaps remaining between file blocks).
For the disk map `12345`, the process looks like this:

```plaintext
0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......
```

The first example requires a few more steps:

```plaintext
00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............
```

The final step of this file-compacting process is to
update the **filesystem checksum**.
To calculate the checksum, add up the result of multiplying each of
these blocks' position with the file ID number it contains.
The leftmost block is in position `0`.
If a block contains free space, skip it instead.

Continuing the first example, the first few blocks' position multiplied by
its file ID number are
`0 * 0 = 0`, `1 * 0 = 0`, `2 * 9 = 18`, `3 * 9 = 27`, `4 * 8 = 32`, and so on.
In this example, the checksum is the sum of these, **`1928`**.

Compact the amphipod's hard drive using the process he requested.
**What is the resulting filesystem checksum?***
*(Be careful copy/pasting the input for this puzzle;*
*it is a single, very long line.)*

**Your puzzle answer was `6382875730645`**.

## Part Two

Upon completion, two things immediately become clear.
First, the disk definitely has a lot more contiguous free space,
just like the amphipod hoped.
Second, the computer is running much more slowly!
Maybe introducing all of that [file system fragmentation][wiki-fs-frag]
was a bad idea?

The eager amphipod already has a new plan:
rather than move individual blocks,
he'd like to try compacting the files on
his disk by moving **whole files** instead.

This time, attempt to move whole files to the leftmost span of
free space blocks that could fit the file.
Attempt to move each file exactly once in order of
**decreasing file ID number** starting with the file with
the highest file ID number.
If there is no span of free space to the left of
a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

```plaintext
00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..
```

The process of updating the filesystem checksum is the same; now,
this example's checksum would be **`2858`**.

Start over,
now compacting the amphipod's hard drive using this new method instead.
**What is the resulting filesystem checksum?**

Your puzzle answer was **`6420913943576`**.

**Both parts of this puzzle are complete!
They provide two gold stars: \*\***

At this point,
you should [return to your Advent calendar][aoc-calendar] and
try another puzzle.

If you still want to see it,
you can [get your puzzle input][aoc-day09-input].

## Learning Points

Be careful with the `range()` function in Python.
I wrote two versions of the `next_free` and `prior_data` functions.
The first ones I tried had the `range()` function in python.

I hadn't noticed how slow it can be sometimes.
So it took a bit to figure it out.
However, in the old `prior_data` function, you can see in the profile below,
that the `range` function when called `23736` times took `35.631` seconds.
That's compared to the new `prior_data` function that took `0.009` seconds.
That's a near `4000x` speedup!

```sh
236210 function calls in 35.723 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        2    0.023    0.012   35.704   17.852 ./2024/09/solve.py:78(defrag1)
    23736   35.631    0.002   35.632    0.002 ./2024/09/solve.py:55(prior_data_old)
    23736    0.016    0.000    0.020    0.000 ./2024/09/solve.py:62(next_free)
    23736    0.018    0.000    0.019    0.000 ./2024/09/solve.py:47(next_free_old)
        2    0.017    0.009    0.019    0.009 ./2024/09/solve.py:25(read_fs)
    23736    0.009    0.000    0.009    0.000 ./2024/09/solve.py:70(prior_data)
   141241    0.008    0.000    0.008    0.000 {built-in method builtins.len}
        2    0.000    0.000    0.000    0.000 {built-in method io.open}
        2    0.000    0.000    0.000    0.000 {method 'read' of '_io.TextIOWrapper' objects}
        2    0.000    0.000    0.000    0.000 /Users/marcus/.local/share/pyenv/versions/3.11.2/lib/python3.11/pathlib.py:546(__fspath__)
        2    0.000    0.000    0.000    0.000 <frozen codecs>:319(decode)
        2    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        2    0.000    0.000    0.000    0.000 <frozen codecs>:309(__init__)
        2    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
        2    0.000    0.000    0.000    0.000 /Users/marcus/.local/share/pyenv/versions/3.11.2/lib/python3.11/pathlib.py:536(__str__)
        2    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
        2    0.000    0.000    0.000    0.000 <frozen codecs>:260(__init__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

### Code Used

The profile comes from comparing different versions of
the `next_free` & `prior_data` functions below using `cprofile`.

```python
def next_free_old(fs: List[int], i: int) -> int:
    for i in range(i, len(fs)):
        if fs[i] == -1:
            return i
    raise ValueError(f"No free space found after {i}")


def prior_data_old(fs: List[int], i: int) -> int:
    # NOTE: Holy shit range() is slow if called thousands+ times in reverse
    for i in range(len(fs) - 1, -1, -1):
        if fs[i] != -1:
            return i
    raise ValueError(f"No data found before {i}")


def next_free(fs: List[int], i: int) -> int:
    while i < len(fs):
        if fs[i] == -1:
            return i
        i += 1
    raise ValueError(f"No free space found after {i}")


def prior_data(fs: List[int], i: int) -> int:
    while i >= 0:
        if fs[i] != -1:
            return i
        i -= 1
    raise ValueError(f"No data found before {i}")


def defrag1(fs: List[int], old_version: bool = False) -> None:
    next_fn = next_free if not old_version else next_free_old
    prior_fn = prior_data if not old_version else prior_data_old
    i_free = next_fn(fs, 0)  # type: ignore
    i_data = prior_fn(fs, len(fs) - 1)  # type: ignore
    while i_free < i_data:
        fs[i_free] = fs[i_data]
        fs[i_data] = -1
        i_free = next_fn(fs, i_free)  # type: ignore
        i_data = prior_fn(fs, i_data)  # type: ignore

```

There's only one change between the old and new versions, the loop statements.
The old versions use the `range()` function in a `for..in..` loop.
Since the profile of the old `next_free` is a reasonable time,
we know it's not the `for..in..`.
The biggest difference is the reversing of a range.
You can see the line that causes the slowdown after the profile:

```python

    for i in range(len(fs) - 1, -1, -1):
```

Somehow reversing the range causes the slowdown.
This warrants some investigating why it's 4000x slower.
It almost defies belief how much slower it is.
Especially since `next_free` with `range` is only `12.5%` slower.

### Profile of Defrag2

Here's the profiler run on `defrag2`.
Note I can't remember if
I was on my M2 Macbook Air on battery or not for the previous ones.
This one I definitely was, so it was in low power mode.

```python
python 09/solve.py -d

Running profiler

Profiling defrag2
         563952797 function calls (563952788 primitive calls) in 141.994 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.018    0.018  141.984  141.984 ./2024/09/solve.py:147(defrag2)
    14924    2.593    0.000  141.939    0.010 ./2024/09/solve.py:134(find_free_space)
  3700379  108.091    0.000  139.065    0.000 ./2024/09/solve.py:64(next_free)
560207052   31.256    0.000   31.256    0.000 {built-in method builtins.len}
    14924    0.022    0.000    0.027    0.000 ./2024/09/solve.py:121(find_last_file)
        1    0.008    0.008    0.009    0.009 ./2024/09/solve.py:26(read_fs)
    14924    0.005    0.000    0.005    0.000 ./2024/09/solve.py:72(prior_data)
        1    0.000    0.000    0.001    0.001 ./2024/.venv/.../rich/console.py:1624(print)
     15/7    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}
```

I notice that `next_free` is still the biggest time sink.
But notably, `len()`, which gets called in `next_free`,
is the second biggest time sink.

Storing the value of `len(fs)` in a variable and using that in
large loops instead works so much better.

```python
 python 09/solve.py -d

Running profiler

Profiling defrag2
         7471100 function calls (7471091 primitive calls) in 63.965 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.018    0.018   63.955   63.955 /Users/marcus/Archive/advent-of-code/2024/09/solve.py:152(defrag2)
    14924    2.202    0.000   63.910    0.004 /Users/marcus/Archive/advent-of-code/2024/09/solve.py:138(find_free_space)
  3700379   61.497    0.000   61.707    0.000 /Users/marcus/Archive/advent-of-code/2024/09/solve.py:67(next_free)
  3725355    0.212    0.000    0.212    0.000 {built-in method builtins.len}
    14924    0.022    0.000    0.027    0.000 /Users/marcus/Archive/advent-of-code/2024/09/solve.py:125(find_last_file)
        1    0.008    0.008    0.009    0.009 /Users/marcus/Archive/advent-of-code/2024/09/solve.py:28(read_fs)
    14924    0.005    0.000    0.005    0.000 /Users/marcus/Archive/advent-of-code/2024/09/solve.py:76(prior_data)
```

Uhh actually I'm getting mixed messages, apparently `len` is constant time.
I think my testing being rushed and not properly controlled is showing here.

Trying `numpy` arrays for all the major functions, I get largely the same:

```sh
python 09/solve_numpy.py
Part 1 example: 1928,         time: 0.285 ms
Part 1 input: 6382875730645,  time: 2821.952 ms
Part 2 example: 2858,         time: 0.492 ms
Part 2 input: 6420913943576,  time: 59771.470 ms

I think any serious improvement requires rethinking the datastractures and having the parser come up with one that stores the data with lengths and ids.
```

## Links

* [Advent of Code - 2023 - Calendar][aoc-calendar]
* [Advent of Code - Day 09 - foobar][aoc-day09]
* [Advent of Code - Day 09 - Input][aoc-day09-input]
* [Advent of Code - Year 2021 - Day 23 - Amphipod][aoc-yr21-day23]
* [Wikipedia - File System Fragmentation][wiki-fs-frag]
<!-- Hidden References -->
[aoc-calendar]: https://adventofcode.com/2024 "Advent of Code - Year/Calendar"
[aoc-day09]: https://adventofcode.com/2024/day/9 "Advent of Code - Day 09"
[aoc-day09-input]: https://adventofcode.com/2024/day/9/input "Advent of Code - Day 04 - Input"
[aoc-yr21-day23]: https://adventofcode.com/2021/day/23 "Advent of Code - Year 2021 - Day 23 - Amphipod"
[wiki-fs-frag]: https://en.wikipedia.org/wiki/File_system_fragmentation "Wikipedia - File System Fragmentation"
