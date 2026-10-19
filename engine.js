// Period Math engine - the same money rate or total, moved between day, week, month and year.
// Mirrored by oracle.py; keep the op order identical.
// Lengths used: 1 week = 7 days, 1 year = 365 days, 1 month = 1/12 of a year. Arithmetic is exact (big integer fractions).
// Amounts are typed with up to 2 decimals, from 0.01 to 1000000. Figures are rounded to 2 decimals, half up.

var UNITS = ["day", "week", "month", "year"];
var LEN = { day: 12n, week: 84n, month: 365n, year: 4380n }; // twelfths of a day

function _unit(u) {
  if (UNITS.indexOf(u) < 0) throw new Error("period must be one of day, week, month, year");
  return u;
}

function _amt(text, label) {
  var t = typeof text === "string" ? text.trim() : "";
  var m = /^([0-9]+)(?:\.([0-9]{1,2}))?$/.exec(t);
  var err = label + " must be a positive number with at most 2 decimals, from 0.01 to 1000000";
  if (!m) throw new Error(err);
  var h = BigInt(m[1]) * 100n + BigInt((m[2] || "") + "00".slice((m[2] || "").length));
  if (h < 1n || h > 100000000n) throw new Error(err);
  return { text: t, h: h };
}

function _count(text) {
  var t = typeof text === "string" ? text.trim() : "";
  var err = "count must be a whole number from 1 to 10000";
  if (!/^[0-9]{1,5}$/.test(t)) throw new Error(err);
  var v = BigInt(t);
  if (v < 1n || v > 10000n) throw new Error(err);
  return v;
}

// n/d hundredths as text: rounded to 2 decimals half up, commas, marked exactly or about.
function _fig(n, d) {
  var s = (2n * n + d) / (2n * d);
  if (s === 0n) return "under 0.01";
  var frac = String(s % 100n);
  while (frac.length < 2) frac = "0" + frac;
  while (frac.length > 0 && frac.charAt(frac.length - 1) === "0") frac = frac.slice(0, -1);
  var whole = String(s / 100n).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return (n % d === 0n ? "exactly " : "about ") + whole + (frac ? "." + frac : "");
}

function _span(count, unit) { return count + " " + unit + (count === 1n ? "" : "s"); }

function _join(parts) {
  if (parts.length === 1) return parts[0];
  return parts.slice(0, -1).join(", ") + " and " + parts[parts.length - 1];
}

// The convert truth: a rate per one period, as the other three periods.
function convertTruth(amount, per) {
  var a = _amt(amount, "amount"), p = _unit(per);
  var parts = [];
  UNITS.forEach(function (u) {
    if (u !== p) parts.push(_fig(a.h * LEN[u], LEN[p]) + " per " + u);
  });
  return a.text + " per " + p + " is " + _join(parts) + ".";
}

// The total truth: what a rate adds up to over a stretch of time.
function totalTruth(amount, per, count, unit) {
  var a = _amt(amount, "amount"), p = _unit(per), c = _count(count), u = _unit(unit);
  return a.text + " per " + p + " for " + _span(c, u) + " adds up to " + _fig(a.h * c * LEN[u], LEN[p]) + " in total.";
}

// The need truth: the rate that reaches a target in a stretch of time.
function needTruth(target, count, unit) {
  var t = _amt(target, "target"), c = _count(count), u = _unit(unit);
  var parts = UNITS.map(function (x) { return _fig(t.h * LEN[x], c * LEN[u]) + " per " + x; });
  return "To reach " + t.text + " in " + _span(c, u) + " takes " + _join(parts) + ".";
}
