#!/usr/bin/env python3
"""Week 4 · Task 3 — Same memory, fewer mistakes.

Textbook §4.4 (Bloom filters), §4.5 (counting distinct).

`NaiveFilter` is a membership filter in a fixed number of bits. It works. It
also makes far more mistakes than it has to with the memory it was given, and
it does so for a reason you can find by reading §4.4.2 and doing one derivative.

You get **exactly the same number of bits**. Make fewer mistakes.

    python3 bench.py
    python3 bench.py --yours

The rule that makes this interesting: a false negative is not allowed. Ever.
The whole point of this structure is that "no" means no. A filter that gets a
better score by occasionally forgetting something it was given has not improved
anything, it has broken the contract.
"""
import hashlib


class NaiveFilter:
    """One hash function, and the bits it was given."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed
        self.bits = bytearray(n_bits)

    def _index(self, item):
        d = hashlib.blake2b(str(item).encode(), digest_size=8,
                            key=str(self.seed).encode()).digest()
        return int.from_bytes(d, "big") % self.n_bits

    def add(self, item):
        self.bits[self._index(item)] = 1

    def __contains__(self, item):
        return bool(self.bits[self._index(item)])

    def memory_bits(self):
        return self.n_bits


class YourFilter:
    """Bloom filter using the same bit budget with an optimal k."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed

        # m/n = 10, so optimal k = (m/n) ln 2 ≈ 6.93
        self.k = 7

        # Actually pack 8 filter bits into one byte.
        self.bits = bytearray((n_bits + 7) // 8)

    def _hashes(self, item):
        data = str(item).encode()

        # Make two independent-looking 64-bit hashes,
        # then use double hashing to generate k positions.
        digest = hashlib.blake2b(
            data,
            digest_size=16,
            key=str(self.seed).encode()
        ).digest()

        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:], "big")

        for i in range(self.k):
            yield (h1 + i * h2) % self.n_bits

    def _set_bit(self, pos):
        byte_index = pos // 8
        bit_index = pos % 8
        self.bits[byte_index] |= (1 << bit_index)

    def _get_bit(self, pos):
        byte_index = pos // 8
        bit_index = pos % 8
        return bool(self.bits[byte_index] & (1 << bit_index))

    def add(self, item):
        for pos in self._hashes(item):
            self._set_bit(pos)

    def __contains__(self, item):
        return all(self._get_bit(pos) for pos in self._hashes(item))

    def memory_bits(self):
        return len(self.bits) * 8