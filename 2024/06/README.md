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

In this example, the guard will visit **(`41`)** distinct positions on your map.

Predict the path of the guard.
**How many distinct positions will the guard visit before**
**leaving the mapped area?**

**Your puzzle answer was `4656`**.

## Part Two

While The Historians begin working around the guard's patrol route,
you borrow their fancy device and step outside the lab.
From the safety of a supply closet,
you time travel through the last few months and [record][aoc-18-day05]
the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians,
they explain that the guard's patrol area is simply too large for them to
safely search the lab without getting caught.

Fortunately, they are **pretty sure** that
adding a single new obstruction **won't** cause a time paradox.
They'd like to place the new obstruction in such a way that
the guard will get **stuck in a loop**,
making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox,
The Historians would like to know **all** of
the possible positions for such an obstruction.
The new obstruction can't be placed at the guard's starting position -
the guard is there right now and would notice.

In the above example, there are only **`6`** different positions where
a new obstruction would cause the guard to get stuck in a loop.
The diagrams of these six situations use `O` to mark the new obstruction,
`|` to show a position where the guard moves up/down,
`-` to show a position where the guard moves left/right,
and `+` to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

```plaintext
....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
```

Option two, put a stack of failed suit prototypes in
the bottom right quadrant of the mapped area:

```plaintext
....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
```

Option three,
put a crate of chimney-squeeze prototype fabric next to the standing desk in
the bottom right quadrant:

```plaintext
....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#.........
......#...
```

Option four, put an alchemical retroencabulator near the bottom left corner:

```plaintext
....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
```

Option five, put the alchemical retroencabulator a bit to the right instead:

```plaintext
....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
```

Option six, put a tank of sovereign glue right next to the tank of universal solvent:

```plaintext
....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#..+----++
......#O..
```

It doesn't really matter what you choose to use as an obstacle so long as
you and The Historians can put it into position without the guard noticing.
The important thing is having enough options that you can find one that
minimizes time paradoxes,
and in this example, there are `**6**` different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction.
**How many different positions could you choose for this obstruction?**

Your puzzle answer was *`1575`*.

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
  * **113555.607 ms**
  * Let's call this the `base` case
* After changing `Guard` to not parse lines every time it took
  * **110783.375 ms**
  * Let's call this case `guard`
* After implementing `candidate_test` with multiprocessing with 4 workers took:
  * **54352.520 ms** (2.04x speedup)
  * Let's call this `mult4`
* After changing workers to 8 it took:
  * 53683.053 ms (1.01x speedup, from 4, 2.04x speedup from None)
  * Let's call this `mult8`
* Reducing MAX_STEPS to 10**5 took:
  * 50088.752 ms (1.07x speedup from 10**6, 2.15x speedup from original)
  * Let's call this max5

Here's a table of the results:

| Name  | Time (s) | Speedup (Base) | Speedup (Inc.) |
|-------|----------|----------------|----------------|
| base  |  113.556 |          1.00x |          1.00x |
| guard |  110.783 |          1.02x |          1.02x |
| mult4 |   54.352 |          2.09x |          2.04x |
| mult8 |   53.683 |          2.11x |          1.03x |
| max5  |   50.089 |          2.26x |          1.07x |

I think the only significant speedup was the multiprocessing.
Going beyond, I think I'd need to fix the loop detection algorithm.
Maybe even pruning out guard states after a certain number of steps.
Maybe even finding a better algorithm in general.

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
