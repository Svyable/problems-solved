# Problems Solved — Research Log

An open research archive for repeated attempts at **unsolved ciphers, undeciphered texts, mathematical conjectures, theorems, and adjacent puzzles**.

The hourly research task publishes a **timestamped log of every attempt**, including negative results, dead ends, useful partial progress, and verified breakthroughs. A research note is **not** a claim that an open problem has been solved.

## Organization

- `runs/YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ.md` — one record for each hourly research attempt (UTC timestamp; safe for parallel/late runs).
- `solutions/<problem-slug>.md` — **only** independently verified or convincingly reproducible, genuinely solved problems or clearly bounded subproblems. If broader results remain unverified, classify them as partial findings in `runs/`.
- `README.md` — methods, conventions, and navigation.

## Required hourly run record

Every entry should report:
1. UTC run time; target problem; exact problem statement and why it is believed open.
2. Primary sources and current known state, with working URLs.
3. Approaches attempted, derivations/code/test cases, and reproducibility commands where possible.
4. Results, including failed attempts, negative tests, counterexamples, and limitations.
5. Confidence and status: **EXPLORATORY**, **PARTIAL / UNVERIFIED**, **REPRODUCED / VERIFIED**, or **SOLVED — INDEPENDENTLY VERIFIED**.
6. Suggested next steps that another run can build on.
7. GitHub commit/PR details if changes cannot be placed directly on the default branch.

Be explicit about what was checked. Do not imply that a conjecture is proven, a historical text deciphered, or a finding novel unless supported by independent checking and a prior-work search. Distinguish a solution to a bounded test instance from a general proof.

## Publishing rules

- Prefer incremental, reviewable commits to `main` when permissions and repository protections allow.
- If branch restrictions prevent direct commits, open a PR with the run log, and enable auto-merge when available; otherwise report the publication blocker.
- Never publish API keys, secrets, private input data, or unsupported claims of scientific breakthroughs.
- Publish routine logs every hour. Reserve celebratory notifications for **interesting, independently supported findings**.

*Automated research can be valuable without producing a proof. Its evidence and failures belong in the record too.*
