# Period Math

Rate per period arithmetic. 5 per day is 1,825 per year, not the 1,800 that 30 days a month suggests.

## What it computes

- **The convert truth** - an amount per day, week, month or year, as the other three.
- **The total truth** - what a rate adds up to over a number of days, weeks, months or years.
- **The need truth** - the rate per day, week, month and year that reaches a target in a stretch of time.

Amounts have up to 2 decimals, from 0.01 to 1000000; counts are whole numbers from 1 to 10000. A week is 7 days, a year is 365 days and a month is one twelfth of a year (about 30.42 days). Arithmetic is exact with big-integer fractions. Figures are rounded to 2 decimals, half up, and marked "exactly" or "about".

## Boundary

Arithmetic only. It assumes the rate stays the same and does not know your real prices, billing dates or fees. Check those against your own bills.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror (Fractions, day lengths 1, 7, 365/12, 365) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (48 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/periodmath/
Repo: https://github.com/iLanis-agent/periodmath
