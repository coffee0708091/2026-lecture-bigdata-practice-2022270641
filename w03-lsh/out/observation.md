The crossover happened somewhere between n=500 and n=1000. In my test, LSH became slightly faster than brute force at n=1000.

When n was doubled, the brute-force runtime increased by roughly four times, so the result matched the expected O(n²) behavior. As the dataset became larger, runtime was the main problem for brute force, while LSH reduced the number of comparisons a lot but used more memory.

For LSH, I used 24 bands with 4 rows in each band. With a similarity of s=0.6, the candidate probability is 1 - (1 - 0.6^4)^24 ≈ 0.964. This means that a pair near the threshold has about a 96.4% chance of becoming a candidate, which seemed like a reasonable trade-off between finding similar pairs and reducing unnecessary comparisons.