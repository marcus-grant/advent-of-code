# Day 08 - Resonant Collinearity

## Part One

You find yourselves on the [roof][aoc-yr16-day25] of
a top-secret Easter Bunny installation.

While The Historians do their thing,
you take a look at the familiar **huge antenna**.
Much to your surprise,
it seems to have been reconfigured to emit a signal that
makes people 0.1% more likely to
buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift!
Unthinkable!

Scanning across the city, you find that there are actually many such antennas.
Each antenna is tuned to a specific **frequency** indicated by
a single lowercase letter, uppercase letter, or digit.
You create a map (your puzzle input) of these antennas.

**For example:**

```plaintext
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
```

The signal only applies its nefarious effect at specific **antinodes** based on
the resonant frequencies of the antennas.
In particular,
an antinode occurs at any point that is perfectly in line with
two antennas of the same frequency -
but only when one of the antennas is twice as far away as the other.
This means that for any pair of antennas with the same frequency,
there are two antinodes, one on either side of them.

So, for these two antennas with frequency `a`,
they create the two antinodes marked with `#`:

```plaintext
..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
```

Adding a third antenna with the same frequency creates several more antinodes.
It would ideally add four antinodes,
but two are off the right side of the map, so instead it adds only two:

```plaintext
..........
...#......

#

....a.....
........a.
.....a....
..#.......
......#...
..........
..........
```

Antennas with different frequencies don't create antinodes;
`A` and `a` count as different frequencies.
However, antinodes **can** occur at locations that contain antennas.
In this diagram, the lone antenna with
frequency capital `A` creates no antinodes but
has a lowercase-`a`-frequency antinode at its location:

```plaintext
..........
...#......

#

....a.....
........a.
.....a....
..#.......
......A...
..........
..........
```

The first example has antennas with two different frequencies,
so the antinodes they create look like this,
plus an antinode overlapping the topmost `A`-frequency antenna:

```plaintext
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........

# #

........A...
.........A..
..........#.
..........#.
```

Because the topmost `A`-frequency antenna overlaps with a `0`-frequency antinode,
there are `**14**` total unique locations that
contain an antinode within the bounds of the map.

Calculate the impact of the signal.
**How many unique locations within the bounds of the map contain an antinode?**

**Your puzzle answer was `371`**.

## Part Two

Watching over your shoulder as you work,
one of The Historians asks if
you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model,
it turns out that an antinode occurs at **any grid position** exactly in line with
at least two antennas of the same frequency, regardless of distance.
This means that some of the new antinodes will occur at the position of
each antenna (unless that antenna is the only one of its frequency).

So, these three `T`-frequency antennas now create many antinodes:

```plaintext
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
```

In fact,
the three `T`-frequency antennas are all exactly in line with two antennas,
so they are all also antinodes!
This brings the total number of antinodes in the above example to `**9**`.

The original example now has `**34**` antinodes,
including the antinodes that appear on every antenna:

```plaintext
##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
# ....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
```

Calculate the impact of the signal using this updated model.
**How many unique locations within the bounds of the map contain an antinode?**

Your puzzle answer was `1229`.

**Both parts of this puzzle are complete!
They provide two gold stars: \*\***

At this point,
you should [return to your Advent calendar][aoc-calendar] and
try another puzzle.

If you still want to see it,
you can [get your puzzle input][aoc-day08-input].

## Links

* [Advent of Code - 2023 - Calendar][aoc-calendar]
* [Advent of Code - Day 08 - Resonant Collinearity][aoc-day08]
* [Advent of Code - Day 08 - Input][aoc-day08-input]
* [Adventure of Code - 2016 - Day 25 - Clock Signal][aoc-yr16-day25]

<!-- Hidden References -->
[aoc-calendar]: https://adventofcode.com/2024 "Advent of Code - Year/Calendar"
[aoc-day08]: https://adventofcode.com/2024/day/8 "Advent of Code - Day 08"
[aoc-day08-input]: https://adventofcode.com/2024/day/8/input "Advent of Code - Day 04 - Input"
[aoc-yr16-day25]: https://adventofcode.com/2016/day/25 "Advent of Code - Year 2016 - Day 25 - Clock Signal"

