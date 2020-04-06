# R2-Challenges

This repo will contain Python 3 challenges along with applicable test cases.

Anyone is free to contribute - either their solutions within the challenge solution folders, or anything else they feel would help to the repo itself.

## Running

A `__main__.py` is included, so feel free to execute it or the directory directory.

If you include the word `verbose` as an arument, you'll get expanded output

***

To run an individual solution, you can execute the solution as a module like so:

`python -m challenges.01.solutions.RascalTwo`

## Adding a solution

I've tried to make it extreamly simple to add and test your solutions - so first clone the repo to your machine.

> If you wish to submit this solution, fork first, then clone your fork

After that, go the challenge you wish to add your solutions too and create a file named your username in the `solutions` directory

> Alternatively, you can copy the [UserName.py](challenge_template/solutions/UserName.py) to the challenge solution folder you wish to submit, and rename it to your username.

All that honestly matters is that the last line of the file is this:

```python
SOLVERS = [name_of_method_that_solves_challenge]
```

***

This allows the testing framework to grab your solutions - think of it as exporting them.

After that, you can run the program and see how your solution does!

> The code within the `if __name__ == '__main__':` block is only required for direct-execution.

## Submitting a Solution

See the [Contributing](CONTRIBUTING.md) guide for how to submit your solution
