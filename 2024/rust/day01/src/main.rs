use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn main() -> io::Result<()> {
    // Collect the command-line arguments
    let args: Vec<String> = env::args().collect();

    // Ensure exactly one argument (the file path) is provided
    if args.len() != 2 {
        eprintln!("Usage: cargo run <file_path>");
        std::process::exit(1);
    }

    let file_path = &args[1];

    // Open the file in read-only mode
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);

    // Read lines into a vector of strings
    let lines: Vec<String> = reader.lines().collect::<Result<_, io::Error>>()?;

    // For demonstration, print the lines (you can remove this)
    for (idx, line) in lines.iter().enumerate() {
        println!("Line {}: {}", idx + 1, line);
    }

    // Split the lines into a left and right vector
    // Each line has two integers separated by arbitrary amounts of whitespace
    let mut left: Vec<i32> = Vec::new();
    let mut right: Vec<i32> = Vec::new();

    // Parse the lines into the left and right vectors
    for (idx, line) in lines.iter().enumerate() {
        // Split line by whitespace
        let parts: Vec<&str> = line.split_whitespace().collect();

        // Ensure at least two parts
        if parts.len() < 2 {
            eprintln!("Line {} does not have two parts", idx + 1);
            std::process::exit(1);
        }

        // Parse first part as left integer
        let xleft: i32 = match parts[0].parse() {
            Ok(num) => num,
            Err(_) => {
                eprintln!(
                    "Error: Unable to parse '{}' as an integer on line {}.",
                    parts[0],
                    idx + 1
                );
                std::process::exit(1);
            }
        };

        // Parse the second part as the right int
        let xright: i32 = match parts[1].parse() {
            Ok(num) => num,
            Err(_) => {
                eprintln!(
                    "Error: Unable to parse '{}' as an integer on line {}.",
                    parts[1],
                    idx + 1
                );
                std::process::exit(1);
            }
        };

        // Push parts into their vectors
        left.push(xleft);
        right.push(xright);
    }

    // Check left and right vectors are formatted correctly
    println!("Left: {:?}", left);
    println!("Right: {:?}", right);

    left.sort();
    right.sort();

    println!("Left sorted: {:?}", left);
    println!("Right sorted: {:?}", right);

    // Create a dictionary to count the number of times an int appears in right vector
    let mut counts: HashMap<i32, i32> = HashMap::new();
    for x in right.iter() {
        *counts.entry(*x).or_insert(0) += 1;
    }

    // Debug counts map
    println!("Counts: {:?}", counts);

    // Iterate through ints in left vector and get counts from right vector
    let mut ans1: i32 = 0;
    for x in left.iter() {
        let mut prod: i32 = 0;
        match counts.get(x) {
            Some(count) => prod = count * x,
            None => (),
        }
        ans1 += prod;
    }

    // Print answer to part 1
    println!("Part 1 Answer: {}", ans1);

    // TODO: Implement Part 2

    Ok(())
}
