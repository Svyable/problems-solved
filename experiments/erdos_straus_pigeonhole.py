#!/usr/bin/env python3
"""Sufficient divisor-residue pigeonhole test; DOES NOT PROVE THE CONJECTURE.

Let p be prime 1 mod 24, a=3+4t<p, x=(p+a)/4.
If divisors of x occupy more than phi(a)/2 distinct unit classes mod a,
two divisor residues are opposites. Then r,s|x with a|(r+s),
giving 4/p = 1/x + 1/[p*(x/r)*k] + 1/[p*(x/s)*k],
where k=(r+s)/a. This script checks the sufficient condition only.
"""
import argparse
from math import gcd
from collections import Counter
from erdos_straus_two_target_dp import sieve, factors

def run(bound=1_000_000, max_shift=35):
    spf=sieve(bound+4*max_shift+4)
    phis={3+4*t:sum(gcd(j,3+4*t)==1 for j in range(3+4*t))
          for t in range(max_shift+1)}
    hist=Counter()
    exceptions=[]
    total=0
    for p in range(73,bound+1,24):
        if spf[p]!=p: continue
        total+=1
        found=False
        for t in range(max_shift+1):
            a=3+4*t
            if a>=p: break
            x=(p+a)//4
            residues={1%a}
            for q,e in factors(x,spf).items():
                residues={r*pow(q,j,a)%a for r in residues for j in range(e+1)}
            if 2*len(residues)>phis[a]:
                hist[t]+=1
                found=True
                break
        if not found: exceptions.append(p)
    print('candidate primes',total,'certified by pigeonhole',sum(hist.values()))
    print('exceptions count',len(exceptions),'exceptions',exceptions)
    print('shifts',dict(sorted(hist.items())))
    assert total==sum(hist.values())+len(exceptions)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--bound',type=int,default=1_000_000)
    ap.add_argument('--max-shift',type=int,default=35)
    a=ap.parse_args()
    run(a.bound,a.max_shift)
