#!/usr/bin/env python3
"""Exact finite search for Erdős–Straus prime certificates, NOT a proof.

For prime p == 1 (mod 24), x=(p+a)/4 with a=3+4*t < p.
Known Bradford-style criterion: some divisor h of x*x satisfies
    h == -x (mod a)       [Type II]
or  4*h == -1 (mod a)     [Type I].
We find such h by dynamic programming over divisor residues modulo a,
then verify 4/p=1/x+1/y+1/z using integers only.
"""
from array import array
from collections import Counter
from math import isqrt
import argparse


def sieve(n):
    spf = array("I", range(n+1))
    for q in range(2, isqrt(n)+1):
        if spf[q] == q:
            for v in range(q*q, n+1, q):
                if spf[v] == v:
                    spf[v] = q
    return spf


def factors(n, spf):
    out = {}
    while n > 1:
        q = spf[n]
        e = 0
        while n % q == 0:
            n //= q
            e += 1
        out[q] = e
    return out


def certificate(p, t, spf):
    a = 3 + 4*t
    if a >= p:
        return None
    x = (p+a)//4
    assert (p+a)%4 == 0 and x < p and x < len(spf)
    states = {1 % a: 1}  # residue -> ONE divisor of x^2
    for q, v in factors(x, spf).items():
        powers = [q**j for j in range(2*v+1)]
        next_states = {}
        for r, h in states.items():
            for power in powers:
                rr = (r*power) % a
                if rr not in next_states:
                    next_states[rr] = h*power
        states = next_states
    h = states.get((-x) % a)
    kind = "II"
    if h is None:
        h = states.get((-pow(4, -1, a)) % a)
        kind = "I"
    if h is None:
        return None
    assert x*x % h == 0
    m = p*x
    d = p*h if kind == "II" else p*p*h
    assert m*m % d == 0
    e = m*m // d
    assert (m+d) % a == 0 and (m+e) % a == 0
    y, z = (m+d)//a, (m+e)//a
    assert x > 0 and y > 0 and z > 0
    assert 4*x*y*z == p*(x*y+x*z+y*z)
    return (x,y,z), kind, h


def scan(bound=1_000_000, max_shift=35):
    spf = sieve(bound+4*max_shift+4)
    total=0
    hist=Counter()
    kind_counts=Counter()
    uncovered=[]
    hardest=None
    for p in range(73, bound+1, 24):
        if spf[p] != p:
            continue
        total += 1
        for t in range(max_shift+1):
            result = certificate(p,t,spf)
            if result is not None:
                triple,kind,h = result
                hist[t] += 1
                kind_counts[kind] += 1
                if hardest is None or t > hardest[1]:
                    hardest = (p,t,triple,kind,h)
                break
        else:
            uncovered.append(p)
    assert total == sum(hist.values())+len(uncovered)
    print("bound",bound,"candidate primes",total,"uncovered",len(uncovered))
    print("least-shift histogram",dict(sorted(hist.items())))
    print("types",dict(kind_counts))
    print("hardest",hardest)
    print("first uncovered",uncovered[:20])


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--bound",type=int,default=1_000_000)
    parser.add_argument("--max-shift",type=int,default=35)
    args=parser.parse_args()
    scan(args.bound,args.max_shift)
