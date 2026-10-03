#!/usr/bin/env python3
"""Week 4 · Task 1 — Answer questions about a stream you cannot store."""

import argparse, random, math, hashlib, statistics


class BloomFilter:
    """Membership, with one-sided error."""

    def __init__(self, m, k, seed=246):
        self.m = m
        self.k = k
        self.seed = seed
        self.bits = bytearray(m)

    def _hashes(self, item):
        s = str(item).encode()

        for i in range(self.k):
            h = hashlib.blake2b(
                s,
                digest_size=8,
                person=f"{self.seed+i}".encode()[:16]
            ).digest()

            value = int.from_bytes(h, "big")
            yield value % self.m

    def add(self, item):
        for pos in self._hashes(item):
            self.bits[pos] = 1

    def __contains__(self, item):
        return all(self.bits[pos] for pos in self._hashes(item))

    def expected_fp_rate(self, n_inserted):
        # textbook approximation:
        # (1 - e^(-kn/m))^k
        return (1 - math.exp(-self.k * n_inserted / self.m)) ** self.k


def flajolet_martin(stream, n_hashes=64, seed=246):
    """Estimate number of distinct items using multiple FM sketches."""

    max_r = [0] * n_hashes

    def trailing_zeros(x):
        if x == 0:
            return 64
        return (x & -x).bit_length() - 1

    for item in stream:
        s = str(item).encode()

        for i in range(n_hashes):
            h = hashlib.blake2b(
                s,
                digest_size=8,
                person=f"{seed+i}".encode()[:16]
            ).digest()

            value = int.from_bytes(h, "big")
            r = trailing_zeros(value)

            if r > max_r[i]:
                max_r[i] = r

    # §4.5.3 style:
    # group estimates, average inside each group,
    # then take median of group averages
    group_size = 8
    group_estimates = []

    for start in range(0, n_hashes, group_size):
        group = max_r[start:start + group_size]

        if not group:
            continue

        estimates = [2 ** r for r in group]

        # 그룹 내부에서 median
        group_estimates.append(statistics.median(estimates))

    # 그룹 결과들을 평균
    return float(sum(group_estimates) / len(group_estimates))

def reservoir_sample(stream, k, seed=246):
    """Uniform reservoir sampling from unknown-length stream."""

    rng = random.Random(seed)
    reservoir = []

    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            # choose uniformly among positions 0..i
            j = rng.randrange(i + 1)

            if j < k:
                reservoir[j] = item

    return reservoir


# ------------------------------------------------------------------- harness
def verify():
    fails = 0
    rng = random.Random(246)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<46} {detail}")
        fails += not ok

    # --- Bloom
    try:
        bf = BloomFilter(m=8192, k=5)
    except NotImplementedError:
        print("  BloomFilter is still a stub"); return 1

    inserted = [f"item-{i}" for i in range(800)]
    for x in inserted:
        bf.add(x)

    check("no false negatives", all(x in bf for x in inserted))

    absent = [f"other-{i}" for i in range(20_000)]
    fp = sum(1 for x in absent if x in bf) / len(absent)

    predicted = bf.expected_fp_rate(len(inserted))
    close = abs(fp - predicted) < max(0.02, predicted * 0.5)

    check(
        "measured false-positive rate matches theory",
        close,
        f"measured {fp:.3%}, predicted {predicted:.3%}"
    )

    # --- Flajolet-Martin
    try:
        distinct = 20_000
        stream = [f"k{rng.randrange(distinct)}" for _ in range(120_000)]
        est = flajolet_martin(stream)
    except NotImplementedError:
        print("  flajolet_martin is still a stub"); return 1

    true_distinct = len(set(stream))
    ratio = est / true_distinct

    check(
        "distinct estimate within a factor of 2",
        0.5 <= ratio <= 2.0,
        f"estimated {est:,.0f}, true {true_distinct:,} ({ratio:.2f}x)"
    )

    # --- Reservoir
    try:
        counts = [0] * 20
        trials = 4000

        for t in range(trials):
            s = reservoir_sample(range(20), 5, seed=t)

            for i in s:
                counts[i] += 1

    except NotImplementedError:
        print("  reservoir_sample is still a stub"); return 1

    expected = trials * 5 / 20
    spread = (max(counts) - min(counts)) / expected

    check(
        "reservoir is uniform across items",
        spread < 0.15,
        f"spread {spread:.1%} around {expected:.0f}"
    )

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())