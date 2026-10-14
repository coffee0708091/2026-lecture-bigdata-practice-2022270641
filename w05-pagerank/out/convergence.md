# Week 5 · Task 2 — PageRank Convergence Analysis

## A1–A3. Beta and Convergence

**Experiment:** 1,200 nodes, tolerance = 1e-10.

| Beta | Iterations | Time (s) |
|---|---:|---:|
| 0.50 | 14 | 0.0289 |
| 0.70 | 17 | 0.0358 |
| 0.85 | 20 | 0.0457 |
| 0.95 | 23 | 0.0436 |
| 0.99 | 24 | 0.0483 |

As beta increases from 0.50 to 0.99, the number of iterations increases from 14 to 24.

A higher beta means the random surfer follows links more frequently and teleports less often. Teleportation helps the rank distribution stabilize, so reducing teleportation generally slows convergence.

The iteration count increases gradually in this graph, rather than becoming extremely large.

## A4. Graph Size Comparison

**Experiment:** Tolerance = 1e-10.

| Beta | Nodes | Iterations | Time (s) |
|---|---:|---:|---:|
| 0.85 | 1,200 | 20 | 0.0457 |
| 0.85 | 20,000 | 21 | 0.6089 |
| 0.95 | 1,200 | 23 | 0.0436 |
| 0.95 | 20,000 | 24 | 0.6867 |

Increasing the graph size by approximately 16.7 times increased the iteration count by only one iteration for both beta values.

However, execution time increased substantially: approximately 13.3 times at beta = 0.85 and 15.7 times at beta = 0.95.

This happens because each iteration must process more nodes and links. Convergence iterations depend on beta, tolerance, and graph structure, rather than increasing directly in proportion to the number of nodes.

## A5. Tolerance and Additional Iterations

**Experiment:** 1,200 nodes, beta = 0.85.

| Tolerance | Iterations | Time (s) |
|---|---:|---:|
| 1e-3 | 7 | 0.0068 |
| 1e-6 | 12 | 0.0112 |
| 1e-10 | 20 | 0.0457 |

A smaller tolerance requires the PageRank values to change less before stopping, resulting in more iterations.

- From 1e-3 to 1e-6: 5 additional iterations over 3 decimal digits, approximately 1.67 iterations per digit.
- From 1e-6 to 1e-10: 8 additional iterations over 4 decimal digits, approximately 2 iterations per digit.

In this experiment, each additional decimal digit of precision required approximately 1.7–2 extra iterations on average.

## A6. Top-10 Ranking Stability

The top-10 page membership remained unchanged across all five beta values, but the order changed.

At beta = 0.50:
- Rank 7: p00000
- Rank 8: p00004

At beta = 0.70:
- Rank 7: p00004
- Rank 8: p00000

The first observed ranking change occurred at beta = 0.70, compared with the previous tested value of 0.50.

The remaining ranking positions stayed unchanged for all tested beta values.

This demonstrates that beta is not only a convergence parameter. It can also influence the final ranking. Therefore, published PageRank rankings depend partly on the chosen beta value, even when the highest-ranked pages remain stable.

## A7. Experimental Environment

CPU: 11th Gen Intel Core i7-1185G7 @ 3.00 GHz
RAM: 15.7 GB
OS: Windows 11
Python: 3.14.3
Development Environment: Visual Studio

Execution times were measured on the local machine and may vary depending on CPU load and background processes. Iteration counts reflect the graph, algorithm, beta, and tolerance used in the experiments.

## Task 2 — Convergence Observations

- As beta increased from 0.50 to 0.99, convergence iterations increased from 14 to 24 because less frequent teleportation generally slows the stabilization of PageRank.
- Increasing graph size from 1,200 to 20,000 nodes increased the iteration count by only one, while execution time increased significantly because each iteration processed more graph data.