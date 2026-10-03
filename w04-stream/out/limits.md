# Task 2 — Exact vs Flajolet-Martin Memory

## Measurements

| Stream size n | True distinct | Exact time | Exact peak memory | FM time | FM peak memory | FM ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 100,000 | 36,702 | 0.23 s | 3.93 MB | 44.57 s | 4.34 KB | 1.28x |
| 400,000 | 146,970 | 1.41 s | 11.59 MB | 197.83 s | 4.22 KB | 0.86x |
| 1,600,000 | 587,625 | 6.85 s | 46.65 MB | 768.98 s | 4.19 KB | 1.31x |
| 3,200,000 | 1,174,671 | 10.49 s | 93.62 MB | 1886.87 s | 4.85 KB | 1.34x |

Additional exact-only measurements:

| Stream size n | True distinct | Exact time | Exact peak memory |
|---:|---:|---:|---:|
| 6,400,000 | 2,349,909 | 18.25 s | 188.38 MB |
| 12,800,000 | 4,699,458 | 43.68 s | 377.66 MB |

## A2 — Where exact became unpleasant

The exact version became unpleasant at n = 12,800,000. It took about 43.7 seconds
and used about 377.7 MB of peak memory.

Memory was the more important long-term limitation because the exact method must
keep every distinct item in a set, so its memory usage continues to grow as the
stream grows.

## A4 — Memory growth

The exact set's peak memory increased approximately linearly with the number of
distinct items.

For example:

- n = 3,200,000 -> 93.62 MB
- n = 6,400,000 -> 188.38 MB
- n = 12,800,000 -> 377.66 MB

Doubling the stream size roughly doubled the exact memory usage.

Flajolet-Martin memory stayed almost constant:

- 4.34 KB
- 4.22 KB
- 4.19 KB
- 4.85 KB

Across the measured 32x stream-size range, exact memory increased from 3.93 MB
to 93.62 MB, about 23.8x, while FM memory changed only about 1.1x.

The reason is that exact counting stores every distinct item, while
Flajolet-Martin stores only a fixed number of hash statistics.

## A5 — Flajolet-Martin accuracy

The FM accuracy ratios were:

- 1.28x
- 0.86x
- 1.31x
- 1.34x

The estimate did not steadily improve or worsen as n increased. The error
fluctuated because Flajolet-Martin is a probabilistic estimator.

All measured estimates remained within a factor of two of the true distinct
count.

## A6 — Machine

Platform: Windows 11
CPU: Intel64 Family 6 Model 140 Stepping 1, GenuineIntel
Python: 3.14.3
RAM: [enter installed RAM]
Other applications running: normal desktop applications