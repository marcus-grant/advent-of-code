# Day 12 - Garden Groups

## Part One

Why not search for the Chief Historian near the [gardener][aoc-2023-day-5] and
his [massive farm][aoc-2023-day-21]?
There's plenty of food,
so The Historians grab something to eat while they search.

You're about to settle near a complex arrangement of garden plots when
some Elves ask if you can lend a hand.
They'd like to set up fences around each region of garden plots,
but they can't figure out how much fence they need to
order or how much it will cost.
They hand you a map (your puzzle input) of the garden plots.

Each garden plot grows only a single type of plant and
is indicated by a single letter on your map.
When multiple garden plots are growing the same type of plant and
are touching (horizontally or vertically), they form a **region**.

**For example:**

```plaintext
AAAA
BBCD
BBCC
EEEC
```

This 4x4 arrangement includes garden plots growing five different types of plant
(labeled `A`, `B`, `C`, `D`, and `E`), each grouped into their own region.

In order to accurately calculate the cost of the fence around a single region,
you need to know that region's **area** and **perimeter**.

The **area** of a region is the count of garden plots it includes.
The above map's type `A`, `B`, and `C` plants are each in a region of area `4`.
The type `E` plants are in a region of area `3`;
the type `D` plants are in a region of area `1`.

Each garden plot is a square and so has **four sides**.
The **perimeter** of a region is the number of sides of garden plots in
the region that do not touch another garden plot in the same region.
The type `A` and `C` plants are each in a region with perimeter `10`.
The type `B` and `E` plants are each in a region with perimeter `8`.
The lone `D` plot forms its own region with perimeter `4`.

Visually indicating the sides of plots in each region that
contribute to the perimeter using `-` and `|`,
the above map's regions' perimeters are measured as follows:

```plaintext
+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|

+ + + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+
```

Plants of the same type can appear in multiple separate regions,
and regions can even appear within other regions.

**For example:**

```plaintext
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
```

The above map contains **five** regions,
one containing all of the `O` garden plots,
and the other four each containing a single `X` plot.

The four `X` regions each have area `1` and perimeter `4`.
The region containing `21` type `O` plants is more complicated;
in addition to its outer edge contributing a perimeter of `20`,
its boundary with each `X` region contributes an additional `4` to
its perimeter, for a total perimeter of `36`.

Due to "modern" business practices,
the **price** of fence required for a region is found by **multiplying** that
region's area by its perimeter.
The **total price** of fencing all regions on a map is found by
adding together the price of fence for every region on the map.

In the first example, region `A` has price `4 * 10 = 40`,
region `B` has price `4 * 8 = 32`, region `C` has price `4 * 10 = 40`,
region `D` has price `1 * 4 = 4`, and region `E` has price `3 * 8 = 24`.
So, the total price for the first example is `**140**`.

In the second example,
the region with all of the `O` plants has price `21 * 36 = 756`,
and each of the four smaller `X` regions has price `1 * 4 = 4`,
for a total price of **`772`** (`756 + 4 + 4 + 4 + 4`).

**Here's a larger example:**

```plaintext
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
```

It contains:

* A region of `R` plants with price `12 * 18 = 216`.
* A region of `I` plants with price `4 * 8 = 32`.
* A region of `C` plants with price `14 * 28 = 392`.
* A region of `F` plants with price `10 * 18 = 180`.
* A region of `V` plants with price `13 * 20 = 260`.
* A region of `J` plants with price `11 * 20 = 220`.
* A region of `C` plants with price `1 * 4 = 4`.
* A region of `E` plants with price `13 * 18 = 234`.
* A region of `I` plants with price `14 * 22 = 308`.
* A region of `M` plants with price `5 * 12 = 60`.
* A region of `S` plants with price `3 * 8 = 24`.

So, it has a total price of **`1930`**.

**Your puzzle answer was `1359028`**.

## Part Two

Fortunately, the Elves are trying to order so much fence that
they qualify for a **bulk discount**!

Under the bulk discount, instead of using the perimeter to calculate the price,
you need to use the **number of sides** each region has.
Each straight section of fence counts as a side, regardless of how long it is.

**Consider this example again:**

```plaintext
AAAA
BBCD
BBCC
EEEC
```

The region containing type `A` plants has `4` sides,
as does each of the regions containing plants of type `B`, `D`, and `E`.
However, the more complex region with the plants of type `C` has `8` sides!

Using the new method of calculating the per-region price by
multiplying the region's area by its number of sides,
regions `A` through `E` have prices `16`, `16`, `32`, `4`, and `12`,
respectively, for a total price of **`80`**.

The second example above (full of type `X` and `O` plants)
would have a total price of `**436**`.

Here's a map that includes an E-shaped region full of type `E` plants:

```plaintext
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
```

The E-shaped region has an area of `17` and `12` sides for a price of `204`.
Including the two regions full of type `X` plants,
this map has a total price of `**236**`.

This map has a total price of `**368**`:

```plaintext
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
```

It includes two regions full of type `B` plants (each with `4` sides) and
a single region full of type `A` plants
(with `4` sides on the outside and `8` more sides on the inside,
a total of `12` sides).
Be especially careful when counting the fence around regions like
the one full of type `A` plants;
in particular, each section of fence has an in-side and an out-side,
so the fence does not connect across the middle of the region
(where the two `B` regions touch diagonally).
(The Elves would have used the Möbius Fencing Company instead,
but their contract terms were too one-sided.)

The larger example from before now has the following updated prices:

* A region of `R` plants with price `12 * 10 = 120`.
* A region of `I` plants with price `4 * 4 = 16`.
* A region of `C` plants with price `14 * 22 = 308`.
* A region of `F` plants with price `10 * 12 = 120`.
* A region of `V` plants with price `13 * 10 = 130`.
* A region of `J` plants with price `11 * 12 = 132`.
* A region of `C` plants with price `1 * 4 = 4`.
* A region of `E` plants with price `13 * 8 = 104`.
* A region of `I` plants with price `14 * 16 = 224`.
* A region of `M` plants with price `5 * 6 = 30`.
* A region of `S` plants with price `3 * 6 = 18`.

Adding these together produces its new total price of **`1206`**.

**What is the new total price of fencing all regions on your map?**

Your puzzle answer was **`839780`**.

**Both parts of this puzzle are complete!
They provide two gold stars: \*\***

At this point,
you should [return to your Advent calendar][aoc-calendar] and
try another puzzle.

If you still want to see it,
you can [get your puzzle input][aoc-day12-input].

## Notes

I started work on a Grid based DFS approach that I think would work well.
I wanted to take that approach because I want to start accumulating
helper snippets or modules to include for common data structures that
get used like `Grids` and `Points` with associated methods.

>**TODO:** Work on at least the `Points` class and associated methods.
>At least next time when a grid shows up.

> **NOTE:** Below the next few sections is the code for the classes so far.

But that's after this portion.
The solution I used to somewhat quickly get through this problem was to
use convolution with the `scipy` & `numpy` libraries.
Since so much is already built I just have to understand the theory.
And here since we're counting perimeters in cardinal directions,
2 convolutions were all that's needed for part 1 and a corner in part 2.

### Setting Up the Grid

Getting connected regions for the problem is really simple by using two methods:

* `np.ndarray.unique` - to get unique values
  * This is used to make an array of unique values in the grid.
  * This is used to iterate over the unique values the next method will use.
* `scipy.ndimage.label` - to get connected regions
  * This creates a binary mask for a given value in the grid.
  * `label(grid == unique_val)`
    * This creates a mask (same size as grid) where:
      * `True` is the value of the unique value in the grid.
      * It's second tuple value is an indexed number for each connected region.
      * Each region is contiguous and we need to handle all of them.

### Calculating Perimeters

Perimeters are easy when you understand **convolution**.
In 2D terms, it's multiplying a larger matrix with a smaller matrix,
usually referred to as a **kernel**.
This kernel gets multiplied over the larger matrix and
it's like a sliding window where you sum the values.
So in essence it's a weighted sum of neighboring values.

Selecting the kernel then gives you the ability to
perform various operations on neighboring values in a matrix.
In this case we care about finding perimeters in a grid of connected regions.
To do this we can use a kernel that looks like this:

```plaintext
  0  1  0
  1  0  1
  0  1  0
```

We can save on computation since we don't care about
the details of the convolution.
We're just using it to calculate a perimeter.
So we'll perform two smaller convolutions that
should result in less computation overall.
We'll use the most basic kernel for horizontal and vertical edge detection.

```plaintext
[[1, -1]]
```

```plaintext
[[1],
 [-1]]
```

These will each find the horizontal and vertical edges respectively.
It makes sense if you look at the shape.
When the convolution is performed across the matrix,
only horizontally neighboring values are weighted and summed.
Same is true for the second kernel, but for vertical neighbors.

When we perform these convolutions and count non-zero values,
those will be values where only a horizontal or vertical transition happened.
This is going to be true of any perimeter that
can only move in cardinal directions.

## Future Work: Grid & Point Class Code

```python
class Location:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
    def __add__(self, other: "Location") -> "Location":
        return Location(self.row + other.row, self.col + other.col)
    def __sub__(self, other: "Location") -> "Location":
        return Location(self.row - other.row, self.col - other.col)
    def __mul__(self, other: "Location") -> "Location":
        return Location(self.row * other.row, self.col * other.col)
    def __floordiv__(self, other: "Location") -> "Location":
        return Location(self.row // other.row, self.col // other.col)
    def __mod__(self, other):
        return Location(self.row % other.row, self.col % other.col)
    def magnitude(self, other: "Location") -> float:
        return ((self.row - other.row) ** 2 + (self.col - other.col) ** 2) ** 0.5
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Location):
            return False
        return self.row == o.row and self.col == o.col
    def __str__(self) -> str:
        return f"({self.row}, {self.col})"
    def __repr__(self) -> str:
        return f"Loc({self.row}, {self.col})"
    def __hash__(self) -> int:
        return hash((self.row, self.col))
    def neighbors(self, diagonal: bool = False) -> List["Location"]:
        ns = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        ns = [Location(*n) for i, n in enumerate(ns) if diagonal or (i % 2)]
        return [self + n for n in ns]
    def is_neighbor(self, other: "Location", diagonal: bool = False) -> bool:
        return True if other in set(self.neighbors(diagonal=diagonal)) else False


class Grid:
    def __init__(
        self,
        # grid: Optional[List[Union[List[str], str]]] = None,
        fpath: Optional[PathLike] = None,
        split_value: Optional[str] = None,
    ) -> None:
        if fpath is not None:
            grid = []
            with open(fpath, "r") as f:
                for line in f.read().splitlines():
                    grid.append(list(line))
            self.grid: List[List[str]] = grid
            self.rows = len(grid)
            self.cols = len(grid[0])
            if any(len(row) != self.cols for row in grid):
                raise ValueError("All rows must be of equal length")
        else:
            raise ValueError("Either grid or fpath must be provided")

    def __getitem__(self, loc: Location) -> str:
        return self.grid[loc.row][loc.col]

    # def __setitem__(self, loc: Location, value: str) -> None:
    #     self.grid[loc.row][loc.col] = value

    def __iter__(self):
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                yield r, c, cell

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    def print(self, col_spacing: int = 0, row_spacing: int = 0) -> None:
        for _, c, cell in self:
            print(cell, end=" " * col_spacing)
            if c == self.cols - 1:
                print()
                if row_spacing > 0:
                    for _ in range(row_spacing):
                        print()

    def inbounds(self, loc: Location) -> bool:
        return 0 <= loc.row < self.rows and 0 <= loc.col < self.cols


def dfs(grid: Grid, origin: Location) -> Set[Location]:
    visited = set()
    neighbors = [n for n in origin.neighbors() if grid.inbounds(n)]
    plot = set()
    while neighbors:
        n = neighbors.pop()
        if n in visited:
            continue
        visited.add(n)
        plot.add(n)
        neighbors.extend([n for n in n.neighbors() if grid.inbounds(n) and grid[]])
    return plot
```

## Links

* [Advent of Code - 2023 - Calendar][aoc-calendar]
* [Advent of Code - Day 12 - Garden Groups][aoc-day12]
* [Advent of Code - Day 12 - Input][aoc-day12-input]
* [Advent of Code - 2023 - Day 5 - If You Give A Seed A Fertilizer][aoc-2023-day-5]
* [Advent of Code - 2023 - Day 21 - Step Counter][aoc-2023-day-21]

<!-- Hidden References -->
[aoc-calendar]: https://adventofcode.com/2024 "Advent of Code - Year/Calendar"
[aoc-day12]: https://adventofcode.com/2024/day/12 "Advent of Code - Day 12"
[aoc-day12-input]: https://adventofcode.com/2024/day/12/input "Advent of Code - Day 04 - Input"
[aoc-2023-day-5]: https://adventofcode.com/2023/day/5 "Advent of Code 2023 - Day 5 - If You Give A Seed A Fertilizer"
[aoc-2023-day-21]: https://adventofcode.com/2023/day/21 "Advent of Code 2023 - Day 21 - Step Counter"
