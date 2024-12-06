# Day 06 - Guard Gallivant

## Part One

The Historians use their fancy [device][aoc-day04] again,
this time to whisk you all away to the North Pole prototype suit manufacturing lab...
in the year [1518][aoc-18-day05]!
It turns out that having direct access to
history is very convenient fora group of historians.

You still have to be careful of time paradoxes,
and so it will be important to avoid anyone from 1518 while
The Historians search for the Chief.
Unfortunately, a single **guard** is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that
The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

```plaintext
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
```

The map shows the current position of the guard with `^`
(to indicate the guard is facing **up** from the perspective of the map).
Any **obstructions** - crates, desks, reactors, etc. - are shown as `#`.

Lab guards in 1518 follow a very strict patrol protocol which
involves repeatedly following these steps:

* If there is something directly in front of you, turn right 90 degrees.
* Otherwise, take a step forward.

Following the above protocol,
the guard moves up several times until she reaches an obstacle
(in this case, a pile of failed suit prototypes):

```plaintext
....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
```

Because there is now an obstacle in front of the guard,
she turns right before continuing straight in her new facing direction:

```plaintext
....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
```

Reaching another obstacle (a spool of several **very** long polymers),
she turns right again and continues downward:

```plaintext
....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
```

This process continues for a while,
but the guard eventually leaves the mapped area
(after walking past a tank of universal solvent):

```plaintext
....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
```

Predicting the guard's route reveals which lab positions are in the patrol path.
**Including the guard's starting position**,
positions visited by the guard before leaving are marked with an `X`:

```plaintext
....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
```

In this example, the guard will visit **`41`** distinct positions on your map.

Predict the path of the guard.
**How many distinct positions will the guard visit before**
**leaving the mapped area?**

**Your puzzle answer was `PLACEHOLDER FOR VERIFIED INPUT ANSWER`**.

## Part Two

***PLACEHOLDER FOR TEXT BEFORE EXAMPLE***

```txt
GO TO URL BELOW, COPY SECOND EXAMPLE TEXT, AND PASTE HERE
https://adventofcode.com/2024/day/6
```

***PLACEHOLDER FOR TEXT AFTER EXAMPLE***

Your puzzle answer was *`PLACEHOLDER FOR VERIFIED INPUT ANSWER`*.

**Both parts of this puzzle are complete!
They provide two gold stars: \*\***

At this point,
you should [return to your Advent calendar][aoc-calendar] and
try another puzzle.

If you still want to see it,
you can [get your puzzle input][aoc-day06-input].

## Optimizations

I implemented several optimizations in the code.

* Before changing the code, the simulator took:
* Let's call this base
* 113555.607 ms
* Before changing Guard to not parse lines every time it took
* Let's call this guard
* 110783.375 ms
* After implementing the candidate test with multiprocessing w/ 4 workers took:
* Let's call this multi4
* 54352.520 ms (2.04x speedup)
* After changing workers to 8 it took:
* Let's call this multi8
* 53683.053 ms (1.01x speedup, from 4, 2.04x speedup from None)
* Reducing MAX_STEPS to 10**5 took:
* Let's call this max5
* 50088.752 ms (1.07x speedup from 10**6, 2.15x speedup from original)

Here's a table of the results:

| Name   | Time (s) | Speedup
|--------|----------|---------
| base   |  113.556 | 1.00x
| guard  |  110.783 | 1.02x
| multi4 |   54.352 | 2.09x
| multi8 |   53.683 | 2.11x
| max5   |   50.089 | 2.26x

I think the only significant speedup was the multiprocessing.
Going beyond, I think I'd need to fix the loop detection algorithm.
Maybe even pruning out guard states after a certain number of steps.
Maybe even finding a better algorithm in general.

```python
# NOTE: Before changing the code, the simulator took:
# 113555.607 ms
# NOTE: Before changing Guard to not parse lines every time it took
# 110783.375 ms
# NOTE: After implementing the candidate test with multiprocessing w/ 4 workers took:
# 54352.520 ms (2.04x speedup)
# NOTE: After changing workers to 8 it took:
# 53683.053 ms (1.01x speedup, from 4, 2.04x speedup from None)
# Move run_candidate to top-level
# NOTE: Reducing MAX_STEPS to 10**5 took:
# 50088.752 ms (1.07x speedup from 10**6, 2.15x speedup from original)
```

## Links

* [Advent of Code - 2023 - Calendar][aoc-calendar]
* [Advent of Code - Day 06 - Guard Gallivant][aoc-day06]
* [Advent of Code - Day 06 - Input][aoc-day06-input]
* [Advent of Code - 2018 - Day 05 - Alchemical Reduction][aoc-18-day05]
* [Advent of Code Day 04 - Ceres Search][aoc-day04]

<!-- Hidden References -->
[aoc-calendar]: https://adventofcode.com/2024 "Advent of Code - Year/Calendar"
[aoc-day06]: https://adventofcode.com/2024/day/6 "Advent of Code - Day 06"
[aoc-day06-input]: https://adventofcode.com/2024/day/6/input "Advent of Code - Day 04 - Input"
[aoc-18-day05]: https://adventofcode.com/2018/day/5 "Advent of Code - 2018 - Day 05 - Alchemical Reduction"
[aoc-day04]: https://adventofcode.com/2024/day/4 "Advent of Code - 2024 - Day 04 - Ceres Search"
