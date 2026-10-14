# Week 5 — PageRank Lab Observations

## Task 1 — PageRank and Its Failures

- In the broken version, a dead-end node has no outgoing links, so its rank disappears during the next iteration. In the fixed version, I redistribute the dead-end rank uniformly across all nodes.
- Teleportation prevents rank from being permanently trapped inside a spider trap, while dead-end redistribution prevents rank from disappearing. Together, these mechanisms keep the rank distribution valid.
- Beta is the probability that the random surfer follows a link. With probability 1 − beta, the surfer teleports to a randomly selected page.

## Task 2 — Convergence Analysis

- As beta increased from 0.50 to 0.99, convergence required 14 to 24 iterations. Higher beta means less teleportation, which generally slows convergence.
- Increasing graph size from 1,200 to 20,000 nodes increased iterations only from 20 to 21 at beta = 0.85, while execution time increased from 0.0457s to 0.6089s. More nodes and edges increase the work per iteration, but iteration count does not grow proportionally with graph size.
- The top-10 membership remained unchanged, but p00000 and p00004 exchanged positions between beta = 0.50 and 0.70. Therefore, the beta value can affect published rankings even when the highest-ranked pages remain stable.

## Task 3 — Sparse PageRank

- Instead of constructing an n × n transition matrix, I used the existing adjacency list and two rank dictionaries. The algorithm requires O(n + m) graph storage and approximately 2n + 5 additional floating-point values, where n is the number of nodes and m is the number of edges.
- Teleportation and dead-end redistribution add the same value to every node. This requires only one pass over n nodes, not an n × n matrix. Actual link contributions are calculated using existing edges.
- The sparse implementation was 49.2× faster and used 598.8× fewer reported floats. The worst per-node difference from the dense result was 1.18e-15, caused by floating-point rounding and the different order of arithmetic operations, not an algorithmic error.