# Day 13 - Claw Contraption

## Part One

Next up: the [lobby][aoc-2020-day24] of a resort on a tropical island.
The Historians take a moment to
admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new [arcade][wiki-arcade]!
Maybe you can win some prizes from the [claw machines][wiki-arcade]?

The claw machines here are a little unusual.
Instead of a joystick or directional buttons to control the claw,
these machines have two buttons labeled `A` and `B`.
Worse, you can't just put in a token and play;
it costs **3 tokens** to push the `A` button and
**1 token** to push the `B` button.

With a little experimentation,
you figure out that each machine's buttons are configured to
move the claw a specific amount to the **right** (along the `X` axis) and
a specific amount **forward** (along `Y` axis) each time that button is pressed.

Each machine contains one **prize**;
to win the prize, the claw must be positioned **exactly** above
the prize on both the `X` and `Y` axes.

You wonder:
what is the smallest number of tokens you would have to
spend to win as many prizes as possible?
You assemble a list of every machine's button behavior and
prize location (your puzzle input).

**For example:**

```plaintext
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
```

This list describes the button configuration and prize location of
four different claw machines.

For now, consider just the first claw machine in the list:

* Pushing the machine's `A` button would move the claw `94` units along
  the `X` axis and `34` units along the `Y` axis.
* Pushing the `B` button would move the claw `22` units along
  the `X` axis and `67` units along the `Y` axis.
* The prize is located at `X=8400`, `Y=5400`;
  this means that from the claw's initial position,
  it would need to move exactly `8400` units along the `X` axis and
  exactly `5400` units along the `Y` axis to be perfectly aligned with
  the prize in this machine.

The cheapest way to win the prize is by pushing the `A` button `80` times and
the `B` button `40` times.
This lines up the claw along the `X` axis (because `80*94 + 40*22 = 8400`) and
along the `Y` axis (because `80*34 + 40*67 = 5400`).
Doing this would cost `80*3` tokens for the `A` presses and
`40*1` for the `B` presses, a total of `**280**` tokens.

>**HINT**: "Half A presses are not allowed."

For the second and fourth claw machines,
there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by
pushing the `A` button `38` times and the `B` button `86` times.
Doing this would cost a total of `**200**` tokens.

So, the most prizes you could possibly win is two;
the minimum tokens you would have to spend to win all (two) prizes is `**480**`.

You estimate that each button would need to
be pressed **no more than `100` times** to win a prize.
How else would someone be expected to play?

Figure out how to win as many prizes as possible.
**What's the fewest tokens you would have to spend to win all possible prizes?**

**Your puzzle answer was `PLACEHOLDER FOR VERIFIED INPUT ANSWER`**.

## Part Two

As you go to win the first prize, you discover that
the claw is nowhere near where you expected it would be.
Due to a unit conversion error in your measurements,
the position of every prize is actually `10000000000000` higher on
both the `X` and `Y` axis!

Add `10000000000000` to the `X` and `Y` position of every prize.
After making this change, the example above would now look like this:

```txt
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
```

Now, it is only possible to win a prize on the second and fourth claw machines.
Unfortunately, it will take **many more than `100` presses** to do so.

Using the corrected prize coordinates,
figure out how to win as many prizes as possible.
**What is the fewest tokens you would have to spend to win all possible prizes?**

Your puzzle answer was **`71493195288102`**.

**Both parts of this puzzle are complete!
They provide two gold stars: \*\***

At this point,
you should [return to your Advent calendar][aoc-calendar] and
try another puzzle.

If you still want to see it,
you can [get your puzzle input][aoc-day13-input].

## Links

* [Advent of Code - 2023 - Calendar][aoc-calendar]
* [Advent of Code - Day 13 - Claw Contraption][aoc-day13]
* [Advent of Code - Day 13 - Input][aoc-day13-input]
* [Advent of Code - 2020 - Day 24 - Lobby Layout][aoc-2020-day24]
* [Wikipedia - Amusement Arcade][wiki-arcade]
* [Wikipedia - Claw Machine][wiki-claw]

<!-- Hidden References -->
[aoc-calendar]: https://adventofcode.com/2024 "Advent of Code - Year/Calendar"
[aoc-day13]: https://adventofcode.com/2024/day/13 "Advent of Code - Day 13"
[aoc-day13-input]: https://adventofcode.com/2024/day/13/input "Advent of Code - Day 04 - Input"
[aoc-2020-day24]: https://adventofcode.com/2020/day/24 "Advent of Code - 2020 - Day 24 - Lobby Layout"
[wiki-arcade]: https://en.wikipedia.org/wiki/Amusement_arcade "Wikipedia: Amusement Arcade"
[wiki-claw]: https://en.wikipedia.org/wiki/Claw_machine "Wikipedia: Claw Machine"
