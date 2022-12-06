# Day 6: Tuning Trouble

*From [Advent of Code][advent-code-22]*
*And from [Day 6][advent-code-22-day-6]*

The preparations are finally complete;
you and the Elves leave camp on foot and
begin to make your way toward the **star** fruit grove.

As you move through the dense undergrowth,
one of the Elves gives you a handheld *device*.
He says that it has many fancy features,
but the most important one to set up right now is the *communication system*.

However,
because he's heard you have
[significant][advent-code-2016-day6]
[experience][advent-code-2016-day25]
[dealing][advent-code-2019-day7]
[with][advent-code-2019-day9]
[signal-based][advent-code-2019-day16]
[systems][advent-code-2021-day25],
he convinced the other Elves that it would be okay to
give you their one malfunctioning *device* -
surely you'll have no problem fixing it.

As if inspired by comedic timing, the *device* emits a few colorful sparks.

To be able to communicate with the Elves,
the *device* needs to *lock on to their signal*.
The *signal* is a series of seemingly-random characters that
the *device* receives one at a time.

To fix the *communication system*,
you need to add a subroutine to the *device* that
detects a start-of-packet marker in the datastream.
In the protocol being used by the Elves,
the start of a packet is indicated by a
sequence of four characters that are all different.

The *device* will send your subroutine a datastream buffer (your puzzle input);
your subroutine needs to identify the first position where
the four most recently received characters were all different.
Specifically,
it needs to report the number of characters from the beginning of the buffer to
the end of the first such four-character marker.

For example, suppose you receive the following datastream buffer:

```txt
mjqjpqmgbljsphdztnvjfqwrcgsmlb
```

After the first three characters (`mjq`) have been received,
there haven't been enough characters received yet to find the marker.
The first time a marker could occur is after the fourth character is received,
making the most recent four characters `mjqj`.
Because `j` is repeated, this isn't a marker.

The first time a marker appears is after the `seventh` character arrives.
Once it does,
the last four characters received are `jpqm`,
which are all different.
In this case, your subroutine should report the value `7`,
because the first start-of-packet marker is complete after
7 characters have been processed.

Here are a few more examples:

- `bvwbjplbgvbhsrlpgdmjqwftvncz`: first marker after character 5
- `nppdvjthqldpwncqszvftbrmjlhg`: first marker after character 6
- `nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg`: first marker after character 10
- `zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw`: first marker after character 11

To begin, get your puzzle input.

*How many characters need to be processed before the first start-of-packet marker is detected?*

Your puzzle answer was `1987`.

That's the right answer!
You are *one gold star* closer to collecting enough star fruit.
[Continue to Part Two][advent-code-22-6-p2]

**The first half of this puzzle is complete! It provides one gold star: ★**

## Part Two

Your device's communication system is correctly detecting packets,
but still isn't working.
It looks like it also needs to look for *messages*.

A *start-of-message* marker is just like a start-of-packet marker,
except it consists of *14 distinct characters* rather than 4.

Here are the first positions of *start-of-message* markers for
all of the above examples:

`mjqjpqmgbljsphdztnvjfqwrcgsmlb`: first marker after character `19`
`bvwbjplbgvbhsrlpgdmjqwftvncz`: first marker after character `23`
`nppdvjthqldpwncqszvftbrmjlhg`: first marker after character `23`
`nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg`: first marker after character `29`
`zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw`: first marker after character `26`

*How many characters need to be processed before the first start-of-message marker is detected?*

Your puzzle answer was `3059`.

That's the right answer! You are **one gold star** closer to collecting enough star fruit.

**The second half of this puzzle is complete! That's two gold stars in total!: ★**

You have completed Day 6! You can [Share][advent-share-mastodon] this victory or
[Return to Your Advent Calendar][advent-code-22]

## References

- [Advent of Code 2022][advent-code-22]
- [Share to Mastodon][advent-share-mastodon]
- [Advent of Code 2022 Day 6 Input][advent-code-22-6-input]
- [Advent of Code 2016 day 6][advent-code-2016-day6]
- [Advent of Code 2016 Day 25][advent-code-2016-day25]
- [Advent of Code 2019 Day 7][advent-code-2019-day7]
- [Advent of Code 2019 Day 9][advent-code-2019-day9]
- [Advent of Code 2019 Day 16][advent-code-2019-day16]
- [Advent of Code 2021 Day 25][advent-code-2021-day25]
- [Advent of Code 2022 Day 6 (Part 2)][advent-code-22-6-p2]

<!-- Hidden Reference Links Below Here -->
[advent-code-22]: https://adventofcode.com/2022 "Advent of Code 2022"
[advent-code-22-day-6]: https://adventofcode.com/2022/day/6
[advent-share-mastodon]: https://fosstodon.org/share?text=I+just+completed+%22Rock+Paper+Scissors%22+%2D+Day+2+%2D+Advent+of+Code+2022+%23AdventOfCode+https%3A%2F%2Fadventofcode%2Ecom%2F2022%2Fday%2F2 "Share to Mastodon"
[advent-code-2016-day6]: https://adventofcode.com/2016/day/6 "Advent of Code 2016 day 6"
[advent-code-2016-day25]: https://adventofcode.com/2016/day/25 "Advent of Code 2016 Day 25"
[advent-code-2019-day7]: https://adventofcode.com/2019/day/7 "Advent of Code 2019 Day 7"
[advent-code-2019-day9]: https://adventofcode.com/2019/day/9 "Advent of Code 2019 Day 9"
[advent-code-2019-day16]: https://adventofcode.com/2019/day/16 "Advent of Code 2019 Day 16"
[advent-code-2021-day25]: https://adventofcode.com/2021/day/25 "Advent of Code 2021 Day 25"
[advent-code-22-6-input]: https://adventofcode.com/2022/day/6/input "Advent of Code 2022 Day 6 Input"
[advent-code-22-6-p2]: https://adventofcode.com/2022/day/6#part2 "Advent of Code 2022 Day 6 (Part 2)"
