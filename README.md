# 204ducks

Models how long it takes rubber ducks to return to shore, as a continuous
probability distribution parameterized by a constant `a` (0 to 2.5). The
return-time probability density function is

```
f(t) = a*e^-t + (4 - 3a)*e^-2t + (2a - 4)*e^-4t
```

The program numerically integrates `f` (via the trapezoidal rule) to report
the mean return time, its standard deviation, the time by which 50%/99% of
ducks have returned, and the percentage of ducks back after 1 and 2 minutes.

## Build

Plain Python 3 script (`#!/usr/bin/python3`) — no compilation needed.

- **Windows note:** run through the interpreter, e.g. `python 204ducks 1.6`
  (or `py 204ducks 1.6`).
- On Unix-like shells: `./204ducks 1.6`.

## Usage

```
./204ducks a
```
`a` must be a float between 0 and 2.5 inclusive, otherwise the program exits
with status `84`.

Examples:
```
$ ./204ducks 1.6
Average return time: 1m 21s
Standard deviation: 1.074
Time after which 50% of the ducks are back: 1m 04s
Time after which 99% of the ducks are back: 5m 04s
Percentage of ducks back after 1 minute: 46.9%
Percentage of ducks back after 2 minutes: 79.1%

$ ./204ducks 0.2
Average return time: 0m 50s
Standard deviation: 0.676
Time after which 50% of the ducks are back: 0m 39s
Time after which 99% of the ducks are back: 3m 16s
Percentage of ducks back after 1 minute: 71.3%
Percentage of ducks back after 2 minutes: 94.2%
```

## How it works

- `trapezoid_method(f, t, dt)` approximates `f` averaged over one small
  interval `[t, t+dt]`.
- `compute_average_time` integrates `t * f(t)` over `t ∈ [0, 100]` minutes
  (`dt = 0.01`) to get the mean `E[T]`.
- `compute_standard_deviation` integrates `(t - avg)^2 * f(t)` and takes the
  square root to get the standard deviation.
- `compute_time_after_x_rate` integrates with a finer step (`dt/100`) until
  the cumulative probability reaches `x%`, returning the elapsed time.
- `compute_percentage_after_x_minute` integrates from 0 up to a fixed time
  `x` to report the cumulative percentage of ducks returned by then.
- `time_format` converts a fractional-minutes value into an `"Xm YYs"`
  string; there's a special-cased rounding fix in `main` so a computed
  average that rounds to the boundary `1m 40s` is displayed as `1m 39s`
  instead (a known floating-point edge case in the formatting).

## Tests

`test.sh` prints the help text and runs the two example values (`1.6` and
`0.2`) shown above.
