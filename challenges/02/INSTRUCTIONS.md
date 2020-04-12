# Password Generator

Given length, digit count, and special count, generate a randomized password of length with the given number of digit and special characters.

---

Your input is one, two, or three integers: length, number of digits, and number of special characters.

The method will take the first number, and optionally digit/special counts, then return a shuffled password of the given length with the given number of characters as digits/specials.

## Input -> Output

The outputs are randomized, but the character quotas are accurate.

- `6` -> `abcdefghi`
- `6, 3` -> `abc123`
- `9, 3, 3` -> `abc123!@#`
- `6, 6` -> `123456`
- `5, 10` -> `12345`
- `0, 3, 3` -> ``
- `0, 0, 1` -> ``
- `1, 2, 3` -> `Exception('Cannot add 2 digit and 3 special characters to a 1 character long password')`

> The exception raised can be of any type, the text content is being tested
