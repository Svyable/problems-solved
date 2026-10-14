#!/usr/bin/env python3
"""Exact, finite Erdos-Straus search for prime p = 1 (mod 24).

Reproduce (Python 3.9+, standard library):
    python3 tools/erdos_straus_factor_search.py --limit 10000000 --max-offset 50 --oracle-limit 1000

This program is NOT a proof of the conjecture and not a novelty claim.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json
from math import isqrt


def spf_table(n):
    spf = list(range(n + 1))
    for k in range(2, isqrt(n) + 1):
        if spf[k] == k:
            for m in range(k * k, n + 1, k):
                if spf[m] == m:
                    spf[m] = k
    return spf


def factor(n, spf):
    result = {}
    while n > 1:
        q = spf[n]
        result[q] = result.get(q, 0) + 1
        n //= q
    return result


def squared_divisors_of_product(p, x, spf):
    exponents = factor(x, spf)
    exponents[p] = exponents.get(p, 0) + 1
    divisors = [1]
    for prime, e in exponents.items():
        old = divisors[:]
        power = 1
        for _ in range(2 * e):
            power *= prime
            divisors += [d * power for d in old]
    return sorted(divisors)


def first_certificate(p, spf, max_offset):
    """Return (offset, (x,y,z), d) or None; complete for tested x values."""
    assert p % 24 == 1 and spf[p] == p, 'p must be prime and 1 mod 24'
    x0 = (p + 3) // 4
    for offset in range(max_offset + 1):
        x = x0 + offset
        r = 4 * x - p
        A = p * x
        if offset == 0:
            # Here A % 3 == 1, r=3. A suitable divisor d of A^2
            # is 2 mod 3 iff x has a prime divisor 2 mod 3.
            candidates = [q for q in factor(x, spf) if q % 3 == 2]
            if not candidates:
                continue
            ds = [min(candidates)]
        else:
            ds = squared_divisors_of_product(p, x, spf)
        for d in ds:
            if d > A:
                break
            if (A + d) % r:
                continue
            Q, remainder = divmod(A * A, d)
            if remainder or (A + Q) % r:
                continue
            y, z = (A + d) // r, (A + Q) // r
            assert 0 < x <= y <= z
            assert 4 * x * y * z == p * (x * y + x * z + y * z)
            return offset, (x, y, z), d
    return None


def independent_brute_offset(p, max_offset):
    """Independent y-enumeration oracle for SMALL p, no factorization."""
    x0 = (p + 3) // 4
    for offset in range(max_offset + 1):
        x = x0 + offset
        A, r = p * x, 4 * x - p
        for y in range(A // r + 1, 2 * A // r + 1):
            numer, denom = A * y, r * y - A
            if denom and numer % denom == 0:
                z = numer // denom
                if y <= z and Fraction(1, x) + Fraction(1, y) + Fraction(1, z) == Fraction(4, p):
                    return offset
    return None


def run(limit, max_offset, oracle_limit):
    spf = spf_table(limit + max_offset + 10)
    hist = Counter()
    failures = []
    sample = {}
    independent_checks = 0
    eligible = 0
    for p in range(73, limit + 1, 24):
        if spf[p] != p:
            continue
        eligible += 1
        result = first_certificate(p, spf, max_offset)
        if result is None:
            failures.append(p)
            continue
        offset, xyz, d = result
        hist[offset] += 1
        if offset not in sample or p > sample[offset]['p']:
            sample[offset] = dict(p=p, x=xyz[0], y=xyz[1], z=xyz[2], d=d)
        if p <= oracle_limit:
            other = independent_brute_offset(p, max_offset)
            assert other == offset, ('oracle mismatch', p, offset, other)
            independent_checks += 1
    return dict(limit=limit, max_offset=max_offset, eligible_prime_count=eligible,
                witnessed=eligible-len(failures), failures=failures,
                offset_histogram={str(k):hist[k] for k in sorted(hist)},
                max_observed_offset=max(hist) if hist else None,
                independent_oracle_checks=independent_checks,
                largest_prime_example_per_offset={str(k):sample[k] for k in sorted(sample)})


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--limit', type=int, default=10_000_000)
    ap.add_argument('--max-offset', type=int, default=50)
    ap.add_argument('--oracle-limit', type=int, default=1_000)
    args = ap.parse_args()
    print(json.dumps(run(args.limit, args.max_offset, args.oracle_limit), indent=2))
