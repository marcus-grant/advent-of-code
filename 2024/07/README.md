# Day 07 - Bridge Repair

## Part One

The Historians take you to a familiar [rope bridge][aoc-yr22-day9] over
a river in the middle of a jungle.
The Chief isn't on this side of the bridge, though;
maybe he's on the other side?

When you go to cross the bridge,
you notice a group of engineers trying to repair it.
(Apparently, it breaks pretty frequently.)
You won't be able to cross until it's fixed.

You ask how long it'll take;
the engineers tell you that it only needs final calibrations,
but some young elephants were playing nearby and **stole all the operators** from
their calibration equations!
They could finish the calibrations if only someone could determine which
test values could possibly be produced by placing any combination of
operators into their calibration equations (your puzzle input).

**For example:**

```plaintext
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
```

Each line represents a single equation.
The test value appears before the colon on each line;
it is your job to determine whether
the remaining numbers can be combined with operators to produce the test value.

Operators are **always evaluated left-to-right**,
**not** according to precedence rules.
Furthermore, numbers in the equations cannot be rearranged.
Glancing into the jungle,
you can see elephants holding two different types of operators:
**add** (`+`) and **multiply** (`**`).

Only three of the above equations can be made true by inserting operators:

* `190: 10 19` has only one position that accepts an operator:
  between `10` and `19`.
  * Choosing `+` would give `29`,
    but choosing `*` would give the test value (`10 * 19 = 190`).
* `3267: 81 40 27` has two positions for operators.
  * Of the four possible configurations of the operators,
    * **two** cause the right side to match the test value:
      * `81 + 40 * 27`
      * `81 * 40 + 27`
    * Both equal `3267` (when evaluated left-to-right)!
* `292: 11 6 16 20` can be solved in exactly one way: `11 + 6 * 16 + 20`.

The engineers just need the **total calibration result**,
which is the sum of the test values from
just the equations that could possibly be true.
In the above example,
the sum of the test values for the three equations listed above is **`3749`**.

Determine which equations could possibly be true.
**What is their total calibration result?**

**Your puzzle answer was `PLACEHOLDER FOR VERIFIED INPUT ANSWER`**.

## Part Two

The engineers seem concerned;
the total calibration result you gave them is nowhere close to
being within safety tolerances.
Just then, you spot your mistake:
some well-hidden elephants are holding a **third type of operator**.

The [concatenation][wiki-concat] operator (`||`) combines the digits from
its left and right inputs into a single number.
For example, `12 || 345` would become `12345`.
All operators are still evaluated left-to-right.

Now, apart from the three equations that
could be made true using only addition and multiplication,
the above example has three more equations that
can be made true by inserting operators:

* `156: 15 6` can be made true through a single concatenation: `15 || 6 = 156`.
* `7290: 6 8 6 15` can be made true using `6 * 8 || 6 * 15`.
* `192: 17 8 14` can be made true using `17 || 8 + 14`.

Adding up all six test values
(the three that could be made before using only `+` and `*` plus the new three that
can now be made by also using `||`)
produces the new **total calibration result** of `**11387**`.

Using your new knowledge of elephant hiding spots,
determine which equations could possibly be true.
**What is their total calibration result?**

```txt
GO TO URL BELOW, COPY SECOND EXAMPLE TEXT, AND PASTE HERE
https://adventofcode.com/2024/day/7
```

***PLACEHOLDER FOR TEXT AFTER EXAMPLE***

Your puzzle answer was *`492383931650959`*.

**Both parts of this puzzle are complete!
They provide two gold stars: \*\***

At this point,
you should [return to your Advent calendar][aoc-calendar] and
try another puzzle.

If you still want to see it,
you can [get your puzzle input][aoc-day07-input].

## Links

* [Advent of Code - 2023 - Calendar][aoc-calendar]
* [Advent of Code - Day 07 - Bridge Repair][aoc-day07]
* [Advent of Code - Day 07 - Input][aoc-day07-input]
* [Advent of Code - 2022 - Day 09 - Rope Bridge][aoc-yr22-day9]

<!-- Hidden References -->
[aoc-calendar]: https://adventofcode.com/2024 "Advent of Code - Year/Calendar"
[aoc-day07]: https://adventofcode.com/2024/day/7 "Advent of Code - Day 07"
[aoc-day07-input]: https://adventofcode.com/2024/day/7/input "Advent of Code - Day 07 - Input"
[aoc-yr22-day9]: https://adventofcode.com/2022/day/9 "Advent of Code - 2022 - Day 09 - Rope Bridge"
[wiki-concat]: https://en.wikipedia.org/wiki/Concatenation "Wikipedia - Concatenation"
