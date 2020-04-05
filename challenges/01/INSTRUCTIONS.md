# Factor Finder

Given a list of numbers and product, find what two factors multiplied together become the given factor.

---

Your input is a list of numbers and a target number.

The method you create should return the two numbers in the list that can be multiplied together to become the target.

There will never be more then one pair of numbers that can be multiplied to become the target number, but there may be none.

The order of the returned numbers does not matter - (10, 7) is just as valid as (7, 10)

## Input -> Output

- `[10, 15, 3, 7], 70` -> `(10, 7)`
- `[8, 2, 6, 3], 18` -> `(6, 3)`
- `[4, 2, 7, 6], 29` -> `None`
- `[26, 8, 385, 687, 9413, 587], 5496` -> `(8, 687)`
