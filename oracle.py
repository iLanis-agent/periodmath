#!/usr/bin/env python3
# Period Math oracle - mirrors engine.js using Fractions, with day lengths as 1, 7, 365/12, 365.
import json, re
from fractions import Fraction

UNITS = ["day", "week", "month", "year"]
DAYS = {"day": Fraction(1), "week": Fraction(7), "month": Fraction(365, 12), "year": Fraction(365)}

def _unit(u):
    if u not in UNITS:
        raise ValueError("period must be one of day, week, month, year")
    return u

def _amt(text, label):
    t = text.strip() if isinstance(text, str) else ""
    m = re.fullmatch(r"([0-9]+)(?:\.([0-9]{1,2}))?", t)
    err = f"{label} must be a positive number with at most 2 decimals, from 0.01 to 1000000"
    if not m:
        raise ValueError(err)
    h = int(m.group(1)) * 100 + int((m.group(2) or "").ljust(2, "0"))
    if h < 1 or h > 100000000:
        raise ValueError(err)
    return t, Fraction(h, 100)  # money

def _count(text):
    t = text.strip() if isinstance(text, str) else ""
    err = "count must be a whole number from 1 to 10000"
    if not re.fullmatch(r"[0-9]{1,5}", t):
        raise ValueError(err)
    v = int(t)
    if v < 1 or v > 10000:
        raise ValueError(err)
    return v

def fig(x):  # x: Fraction money
    s = int((x * 100 * 2 + 1) // 2)
    if s == 0:
        return "under 0.01"
    whole, frac = divmod(s, 100)
    fr = f"{frac:02d}".rstrip("0")
    return ("exactly " if (x * 100).denominator == 1 else "about ") + f"{whole:,}" + ("." + fr if fr else "")

def span(c, u):
    return f"{c} {u}" + ("" if c == 1 else "s")

def join(parts):
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]

def convert_truth(amount, per):
    t, m = _amt(amount, "amount"); p = _unit(per)
    per_day = m / DAYS[p]
    parts = [f"{fig(per_day * DAYS[u])} per {u}" for u in UNITS if u != p]
    return f"{t} per {p} is {join(parts)}."

def total_truth(amount, per, count, unit):
    t, m = _amt(amount, "amount"); p = _unit(per); c = _count(count); u = _unit(unit)
    total = m / DAYS[p] * (c * DAYS[u])
    return f"{t} per {p} for {span(c, u)} adds up to {fig(total)} in total."

def need_truth(target, count, unit):
    t, m = _amt(target, "target"); c = _count(count); u = _unit(unit)
    per_day = m / (c * DAYS[u])
    parts = [f"{fig(per_day * DAYS[x])} per {x}" for x in UNITS]
    return f"To reach {t} in {span(c, u)} takes {join(parts)}."

FNS = {"convertTruth": convert_truth, "totalTruth": total_truth, "needTruth": need_truth}
CASES = [
    ("convertTruth", ["5", "day"]), ("convertTruth", ["100", "week"]), ("convertTruth", ["1200", "month"]), ("convertTruth", ["60000", "year"]),
    ("convertTruth", ["0.01", "year"]), ("convertTruth", ["0.01", "day"]), ("convertTruth", ["1000000", "year"]), ("convertTruth", ["1000000", "day"]),
    ("convertTruth", ["4.99", "month"]), ("convertTruth", ["15.5", "week"]), ("convertTruth", [" 7 ", "day"]), ("convertTruth", ["365", "year"]),
    ("convertTruth", ["12", "month"]), ("convertTruth", ["0", "day"]), ("convertTruth", ["-5", "day"]), ("convertTruth", ["abc", "day"]),
    ("convertTruth", ["5.555", "day"]), ("convertTruth", ["1000000.01", "day"]), ("convertTruth", ["5", "hour"]), ("convertTruth", ["", "day"]),
    ("totalTruth", ["5", "day", "1", "year"]), ("totalTruth", ["5", "day", "3", "month"]), ("totalTruth", ["100", "week", "1", "month"]), ("totalTruth", ["10", "week", "52", "week"]),
    ("totalTruth", ["4.99", "month", "12", "month"]), ("totalTruth", ["4.99", "month", "1", "year"]), ("totalTruth", ["0.01", "year", "1", "day"]), ("totalTruth", ["1000000", "year", "10000", "year"]),
    ("totalTruth", ["2", "day", "1", "week"]), ("totalTruth", ["2", "day", "1", "day"]), ("totalTruth", ["19.99", "month", "18", "month"]), ("totalTruth", ["5", "day", "0", "year"]),
    ("totalTruth", ["5", "day", "10001", "day"]), ("totalTruth", ["5", "day", "1.5", "year"]), ("totalTruth", ["5", "fortnight", "1", "year"]), ("totalTruth", ["5", "day", "1", "decade"]),
    ("needTruth", ["1000", "6", "month"]), ("needTruth", ["1000", "1", "year"]), ("needTruth", ["5000", "52", "week"]), ("needTruth", ["0.01", "10000", "year"]),
    ("needTruth", ["1000000", "1", "day"]), ("needTruth", ["250", "1", "week"]), ("needTruth", ["1200", "1", "month"]), ("needTruth", ["99.99", "7", "day"]),
    ("needTruth", ["1000", "0", "month"]), ("needTruth", ["abc", "6", "month"]), ("needTruth", ["1000", "6", "era"]), ("needTruth", ["1000", "x", "month"]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
