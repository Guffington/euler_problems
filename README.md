# Solutions to the Euler Problems

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Project Euler](https://img.shields.io/badge/Project%20Euler-40%20problems-orange)
![Last Commit](https://img.shields.io/github/last-commit/Guffington/euler_problems)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

Welcome to my collection of solutions to the first 30 Project Euler problems. This repository is part of my programming portfolio and showcases my approach to solving algorithmic and mathematical challenges in Python.

## About Project Euler

Project Euler is a platform offering a series of challenging mathematical and computational problems. Solving these problems enhances algorithmic thinking, mathematical reasoning, and coding proficiency.

[Project Euler Archives](https://projecteuler.net/archives)

## Learning Objectives

Through these problems, I aimed to:

- **Python proficiency:** Continually improve coding skills in Python.

- **Algorithmic thinking:** Develop efficient algorithms for mathematical challenges.

- **Problem solving:** Improve problem-solving strategies and debugging skills.

## Repository Structure

The repository is organized as follows:

```text
euler_problems/
├── problems_1_to_10.py           # Solutions to problems 1–10
├── problems_11_to_20.py          # Solutions to problems 11–20
├── problems_21_to_30.py          # Solutions to problems 21–30
├── problems_31_to_40.py          # Solutions to problems 31–40
├── utils.py                      # Shared helper functions
├── problem_eightn_number.txt     # Input data for Problem 8
├── problem_eleven_number.txt     # Input data for Problem 11
├── problem_thirteen_numbers.txt  # Input data for Problem 13
├── problem_eighteen_triangle.txt # Input data for Problem 18
└── problem_twentytwo_names.txt   # Input data for Problem 22
```

## Getting Started

To run the solutions locally:

### Clone the repository:

```bash
git clone https://github.com/Guffington/euler_problems.git
cd euler_problems
```

#### Runs on Python 3!

### Execute a solution set:

E.g.:

```bash
python3 problems_1_to_10.py
```

This will print out the solutions to problems 1 through 10 in order:

```text
The answer to problem one is: 233168    (Run in 0.00016 s)
The answer to problem two is: 4613732    (Run in 0.00001 s)
...
The answer to problem ten is: 142913828922    (Run in 0.32453 s)
```

Each solution is written within its own named function.

```python
def problem_one(n):
    """
    Returns the sum of all multiples of 3 or 5 below n.
    """
...

answer, time = problem_one(1000)
print(f"The answer to problem one is: {answer}    (Run in {time:.5f} s)")
```

Comment out the function call (below each function) to stop computing a particular solution.

## Future Plans

I intend to continue solving additional Project Euler problems and expand this repository.  
Future updates will include:

- Solutions to problems 41 and beyond.

- Optimizations and refactorings of existing solutions.
