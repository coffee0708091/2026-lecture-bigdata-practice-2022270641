# Task 2 — Crossover Measurement

## Timing results

| n | Brute-force time | LSH time | Brute comparisons | LSH comparisons |
|---:|---:|---:|---:|---:|
| 250 | 0.24 s | 0.89 s | 31,125 | 200 |
| 500 | 1.00 s | 1.80 s | 124,750 | 724 |
| 1000 | 3.99 s | 3.43 s | 499,500 | 3,045 |
| 2000 | 17.98 s | 6.86 s | 1,999,000 | 12,170 |
| 2120 | 19.55 s | 9.03 s | 2,246,140 | 13,841 |

## A4 — Quadratic check

The brute-force runtime approximately quadrupled whenever n doubled.

- 250 → 500: 0.24 s → 1.00 s, about 4.17×
- 500 → 1000: 1.00 s → 3.99 s, about 3.99×
- 1000 → 2000: 3.99 s → 17.98 s, about 4.51×

Therefore, the measurements are consistent with quadratic O(n²) behavior.

## A5 — Peak memory

At the largest actual dataset size, n=2120:

- Brute-force peak memory: 29,544 bytes

- LSH peak memory: 10,354,512 bytes

LSH used considerably more memory because it stores MinHash signatures, band buckets, and candidate pairs, while brute force performs comparisons directly without maintaining those additional structures.

## A6 — Machine

The experiment was run on Windows 11 with an Intel64 processor using Python 3.14.3. Other normal applications were running during the experiment.

## A7 — Crossover

At small n, brute force was faster because it has very little setup overhead.

- n=250: brute force was faster (0.24 s vs 0.89 s)
- n=500: brute force was faster (1.00 s vs 1.80 s)
- n=1000: LSH became faster (3.43 s vs 3.99 s)

Therefore, the crossover occurred between n=500 and n=1000. Among the measured points, n=1000 was the first point where LSH became faster.

## A8 — Why LSH loses at small n

LSH has additional setup cost before exact comparisons are performed. It must compute MinHash signatures for all documents, divide the signatures into bands, and place documents into buckets.

These operations are approximately linear in the number of documents, but they are not free. For small datasets, brute force can finish before the cost of building the LSH structure is recovered.

As n becomes larger, the quadratic growth of brute-force pairwise comparisons dominates, while LSH compares only a much smaller set of candidate pairs.

At n=2120, brute force performed 2,246,140 comparisons, while LSH performed only 13,841 comparisons.

## Dataset-size note

The provided `bench.py` generates 2,000 base documents and 120 planted near-duplicates, for a maximum of 2,120 actual documents. Therefore, requested sizes above 2,120 reuse the full 2,120-document dataset rather than creating additional documents.