# Task 1
A Bloom filter has no false negatives because every inserted item sets all of its hash positions to 1; my predicted false-positive rate was 0.860% and the measured rate was 0.980%. For Flajolet-Martin, grouped medians reduced the effect of large outliers and estimated 21,504 distinct items for a true count of 19,953. Reservoir sampling kept only k items while giving each stream item the same final inclusion probability k/n.

# Task 2
Exact counting became unpleasant at n = 12,800,000, taking about 43.7 seconds and 377.7 MB of peak memory, while Flajolet-Martin stayed around only 4–5 KB. Exact memory grew roughly linearly with stream size, but FM memory stayed nearly constant and its accuracy ratios ranged from 0.86x to 1.34x. A factor-of-two estimate is acceptable for rough traffic monitoring, but not for billing or exact accounting.

# Task 3
With 10 bits per item, the optimal Bloom filter uses k = (m/n) ln 2 ≈ 6.93, so I used 7 hash functions. The theoretical false-positive floor is about 0.82%, and the measured rate was also 0.820% with zero false negatives. If n were unknown, guessing too low would increase false positives, while guessing too high would waste memory.