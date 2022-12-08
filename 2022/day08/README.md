# Day 8: Treetop Tree House

*From [Advent of Code][advent-code-22]*
*For [Day 8 of Year 2022][advent-code-22-day-8]*

## Part One

The expedition comes across a peculiar patch of
tall trees all planted carefully in a grid.
The Elves explain that a
previous expedition planted these trees as a reforestation effort.
Now,
they're curious if this would be a good location for a [tree house][treehouse-wiki].

First,
determine whether there is enough tree cover here to keep a tree house *hidden*.
To do this,
you need to count the number of trees that are *visible from outside the grid*
when looking directly along a row or column.

The Elves have already launched a [quadcopter][quadcopter-wiki] to
generate a map with the height of each tree (your puzzle input).
For example:

```txt
30373
25512
65332
33549
35390
```

Each tree is represented as a single digit whose value is its height,
where `0` is the shortest and `9` is the tallest.

A tree is *visible* if all of the other trees between it and an edge of the grid
are *shorter* than it.
Only consider trees in the same row or column;
that is,
only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are *visible* -
since they are already on the edge,
there's no trees to block the view.
In this example,
that only leaves the *interior nine trees* to consider:

- The top-left `5` is *visible* from the left and top.
(It isn't visible from the right or
bottom since other trees of height 5 are in the way.)
- The top-middle `5` is *visible* from the top and right.
- The top-right `1` is not visible from any direction;
for it to be visible,
there would need to only be trees of height *`0`* between it and an edge.
- The left-middle `5` is visible, but only from the right.
- The center `3` is not visible from any direction;
for it to be visible,
there would need to be only trees of at most height `2` between it and an edge.
- The right-middle `3` is *visible* from the right.
- In the bottom row,
the middle `5` is *visible*,
but the `3` and `4` are not.

With 16 trees *visible* on the edge and another 5 *visible* in the interior,
a total of `21` trees are *visible* in this arrangement.

Consider your map;
*how many trees are visible from outside the grid?*

To begin, [get your puzzle input][advent-code-22-day8-input].

Your puzzle answer was `1829`.

That's the right answer! You are **one gold star closer** to collecting enough star fruit.
[Continue to Part Two]

**The first half of this puzzle is complete! It provides one gold star: ★**

## Part Two

<!-- START Pasted Instructions -->
<!-- END Pasted Instructions -->
*ITALICIZE THE QUESTION PROMPT*

Your puzzle answer was `SOME_ANSWER HERE IN CODE SPAN`.

**The second half of this puzzle is complete! That's two gold stars in total!: ★**

You have completed Day 8! You can [Share][advent-share-mastodon] this victory or
[Return to Your Advent Calendar][advent-code-22]

## References

- [Advent of Code 2022][advent-code-22]
- [Share to Mastodon][advent-share-mastodon]
- [Tree House (from Wikipedia, the free encyclopedia)][treehouse-wiki]
- [Quadcopter (from Wikipedia, the free encyclopedia)][quadcopter-wiki]
- [Advent of Code 2022 Day 8 Input][advent-code-22-day8-input]
- [Advent of Code 2022 Day 8 Part 2][advent-code-22-day8-part2]

<!-- Hidden Reference Links Below Here -->
[advent-code-22]: https://adventofcode.com/2022 "Advent of Code 2022"
[advent-code-22-day-8]: https://adventofcode.com/2022/day/8
[advent-share-mastodon]: https://fosstodon.org/share?text=I+just+completed+%22Rock+Paper+Scissors%22+%2D+Day+2+%2D+Advent+of+Code+2022+%23AdventOfCode+https%3A%2F%2Fadventofcode%2Ecom%2F2022%2Fday%2F2 "Share to Mastodon"
[treehouse-wiki]: https://en.wikipedia.org/wiki/Tree_house "Tree House (from Wikipedia, the free encyclopedia)"
[quadcopter-wiki]: https://en.wikipedia.org/wiki/Quadcopter "Quadcopter (from Wikipedia, the free encyclopedia)"
[advent-code-22-day8-input]: https://adventofcode.com/2022/day/8/input "Advent of Code 2022 Day 8 Input"
[advent-code-22-day8-part2]: https://adventofcode.com/2022/day/8#part2 "Advent of Code 2022 Day 8 Part 2"
