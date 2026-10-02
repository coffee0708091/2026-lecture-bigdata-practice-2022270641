#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """MinHash + LSH near-duplicate finder."""

    def __init__(self, threshold):
        self.threshold = threshold

        # 96 hashes = 24 bands × 4 rows
        self.num_hashes = 96
        self.bands = 24
        self.rows = 4

        # deterministic hash parameters
        self.prime = 1000003

        self.a = [
            (17 * i + 31) % self.prime or 1
            for i in range(self.num_hashes)
        ]
        self.b = [
            (97 * i + 53) % self.prime
            for i in range(self.num_hashes)
        ]

    def _signature(self, doc):
        """Create a MinHash signature for one shingle set."""
        sig = []

        for a, b in zip(self.a, self.b):
            min_hash = min(
                ((a * x + b) % self.prime)
                for x in doc
            )
            sig.append(min_hash)

        return sig

    def find(self, docs, similarity):
        # 1. MinHash signatures
        signatures = [
            self._signature(doc)
            for doc in docs
        ]

        # 2. LSH banding
        candidates = set()

        for band in range(self.bands):
            buckets = {}

            start = band * self.rows
            end = start + self.rows

            for i, sig in enumerate(signatures):
                key = tuple(sig[start:end])

                if key not in buckets:
                    buckets[key] = []

                buckets[key].append(i)

            # Documents in the same bucket become candidate pairs
            for bucket in buckets.values():
                if len(bucket) < 2:
                    continue

                for x in range(len(bucket)):
                    for y in range(x + 1, len(bucket)):
                        i = bucket[x]
                        j = bucket[y]
                        candidates.add((min(i, j), max(i, j)))

        # 3. Exact Jaccard only for candidate pairs
        out = set()

        for i, j in candidates:
            if similarity(docs[i], docs[j]) >= self.threshold:
                out.add((i, j))

        return out